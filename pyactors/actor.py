__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__license__ = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

import sys
import uuid
import logging

from pyactors.inbox import DequeInbox
from pyactors.exceptions import EmptyInbox
from pyactors.exceptions import StopReceived

class BaseActor(object):
    ''' Base class for creating Actors
    '''
    pass

class Actor(object):
    ''' Actor 
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        # actor's name
        if not name:
            self._name = self.__class__.__name__
        else:
            self._name = name
 
        # actor address
        self.address = uuid.uuid4().hex

        if logger is None:
            self.logger = logging.getLogger('%s.Actor' % __name__)
        else:
            self.logger = logger

        # actor's inbox, DequeInbox is default inbox.
        # You can reassign inbox in your Actor class
        self.inbox = DequeInbox()
 
        # actor's parent
        self.parent = None

        # actor's children
        self._children = dict()
        
        # processing
        self._processing = False        
        
        # running process
        self._running = None
        
        # if True, stopping process active
        self._stopping = False

    def __str__(self):
        ''' represent actor as string
        '''
        return u'%(name)s[%(address)s]' % {u'name': self._name, u'address': self.address }    

    @property
    def name(self):
        ''' return actor name
        '''
        return self._name

    @property
    def children(self):
        ''' return list of actor's children
        '''
        return self._children.values()

    def on_start(self):
        ''' on start event handler
        '''
        pass

    def start(self):
        ''' start actor 
        '''
        self._processing = True
        self._running =self.run() 
        
        # start child-actors
        for child in self.children:
            child.start()

        try:
            self.on_start()
        except:
            self._handle_failure(*sys.exc_info())

    def on_receive(self, message):
        ''' on receive message handler 
        '''
        pass

    def on_handle(self):
        ''' on handle event 
        '''
        pass

    def send(self, message):
        ''' send message to actor
        '''
        if not self._stopping:
            self.inbox.put(message)
        else:
            raise StopReceived
    
    def on_stop(self):
        ''' on stop event handler
        '''
        pass

    def stop(self):
        ''' stop actor 
        '''
        self._stopping = True
        # stop child-actors
        for child in self.children:
            # child.stop()
            stop_message = { 'system-msg': {'type': 'stop', 'sender': self.address } }
            child.send(stop_message)
        
    def on_failure(self, exception_type, exception_value, traceback):
        ''' on failure event handler
        '''
        pass

    def _handle_system_message(self, message):
        ''' handle system message 
        '''
        self.logger.debug('%s._handle_system_message(), message: %s' % (self.name, message))
        if not isinstance(message, dict):
            self.logger.debug('%s._handle_system_message(), incorrect system message: %s' % (self.name, message))
            return
        
        msg_type = message.get('type', None)
        sender = message.get('sender','')
        if msg_type and msg_type == 'stop' and sender == self.parent.address:
            self.stop()
            self.logger.debug('%s._handle_system_message(), message "stop" received' % self.name)

    def _handle_message(self, message):
        ''' handle pyactors message
        
        returns True if the message is pyactors (system) message
        '''
        self.logger.debug('%s._handle_message(), message: %s' % (self.name, message))
        if isinstance(message, dict) and message.get('system-msg', None):
            self._handle_system_message(message['system-msg'])         
            return
               
        self.on_receive(message)

    def _handle_failure(self, exception_type, exception_value, traceback):
        ''' handle failure
        '''
        self.logger.error('Unhandled exception in %s' % self,
                           exc_info=(exception_type, exception_value, traceback))
        self.on_failure(exception_type, exception_value, traceback)
        self._processing = False

    def add_child(self, actor):
        ''' add actor's child
        '''
        if actor not in self.children:
            actor.parent = self
            self._children[actor.address] = actor
        else:
            raise RuntimeError('Actor exists: %s', actor)
    
    def remove_child(self, address):
        ''' remove child by its address
        '''
        if address in self._children.keys():
            child = self._children.pop(address)
            child.stop()
        else:
            raise RuntimeError('Actor does not exist, address: %s', address)

    def _processing_loop(self):
        ''' processing loop
        '''
        while self._processing:
            # if inbox is empty and 'stop' command received -> stop processing
            if self._stopping and len(self.inbox) == 0:
                break

            try:
                message = self.inbox.get()
            except EmptyInbox:
                message = None

            if message:
                try:
                    self._handle_message(message)
                except:
                    self._handle_failure(*sys.exc_info())
            
            try:    
                self.on_handle()
            except:
                self._handle_failure(*sys.exc_info())
            yield
            
    def _supervise_loop(self):
        ''' supervise loop
        '''
        while self._processing:
            for child in self.children:
                self.logger.debug('%s.supervise_loop(), child.run_once(): %s' % (self.name, child))
                if not child.run_once():
                    # child completed its job, remove it from children list
                    self._children.pop(child.address)
            if len(self.children) == 0:
                self.logger.debug('%s.supervise_loop(), no active children ' % self.name)
                break
            yield
    
    def run(self):
        ''' run actor 
        
        this method is used only when actor should be started as main one
        '''
        self.logger.debug('%s.run(), started' % self.name)
            
        processing_loop = self._processing_loop()
        supervise_loop = self._supervise_loop()

        while self._processing:

            # processing_loop
            if processing_loop is not None:
                self.logger.debug('%s.run(), processing started' % self.name)
                try:
                    processing_loop.next()
                    self.logger.debug('%s.run(), processing on hold' % self.name)
                except StopIteration:
                    self.logger.debug('%s.run(), processing completed' % self.name)
                    processing_loop = None

            # supervise_loop        
            if supervise_loop is not None:
                self.logger.debug('%s.run(), supervising started' % self.name)
                try:
                    supervise_loop.next()
                    self.logger.debug('%s.run(), supervising on hold' % self.name)
                except StopIteration:
                    self.logger.debug('%s.run(), supervising completed' % self.name)
                    supervise_loop = None

            yield True
        
        self.logger.debug('%s.run(), processing_loop completed' % self.name)
        self.logger.debug('%s.run(), supervise_loop completed' % self.name)
        
        try:
            self.on_stop()
        except:
            self._handle_failure(*sys.exc_info())
        
        yield False
        
    def run_once(self):
        ''' run actor once
        '''
        if self._running is None:
            return False
            
        return self._running.next()

    def join(self):
        ''' wait until actor finished
        '''
        pass
        '''
        while True:
            if not self.run_once():
                break
        '''
            
    def find(self, address=None, actor_class=None, actor_name=None):
        """ find children by criterias 
        
        - if no criterias are defined, return all children addresses
        
        - if `address` is defined as string or unicode, return an actor by its address.
        - if `address` is defined as list or tuple, return actors by thier addresses.
        
        - if actor_class is defined as string or unicode, return the list of all 
        existing actors of the given class, or of any subclass of the given class.
        - if actor_class is defined as list or tuple, return actors by thier actor classes.
        
        - if actor_name is defined, return the list of all existing actors of 
        the given name.
        
        return existing actors by criterias.
        """
        known_actors = list()
        known_actors.extend(self.children)
        if self.parent:
            known_actors.append(self.parent)
            known_actors.extend(self.parent.find(address, actor_class, actor_name))
        known_actors = list(set(known_actors))
        result = list()

        if address:
            # when address is only one
            if isinstance(address, (str, unicode)):
                result.extend([actor for actor in known_actors if actor.address == address])
            # when address if multiple
            elif isinstance(address, (list, tuple)):
                result.extend([actor for actor in known_actors if actor.address in address])
            return result
                                
        if actor_class:
            result.extend([actor for actor in known_actors if isinstance(actor, actor_class)])
            return result
        
        if actor_name:
            result.extend([actor for actor in known_actors if actor._name == actor_name])
            return result
        
        return known_actors

