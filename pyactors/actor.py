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
from pyactors.exceptions import EmptyInboxException

# Actor Family
AF_GENERATOR    = 0
AF_GREENLET     = 1
AF_THREAD       = 2
AF_PROCESS      = 3

class Actor(object):
    ''' Base class for creating Actors 
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        # actor's name
        if not name:
            self._name = self.__class__.__name__
        else:
            self._name = name
 
        # actor family
        self._family = None

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

    @property
    def family(self):
        ''' return actor family
        '''
        if self._family is None:
            raise RuntimeError('Actor family is not specified, %s' % self._name)
        return self._family

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
            

    def on_receive(self, message):
        ''' on receive message handler 
        '''
        pass

    def on_send(self):
        ''' on send message handler 
        '''
        pass

    def send(self, message):
        ''' send message to actor
        '''
        self.inbox.put(message)

    def on_stop(self):
        ''' on stop event handler
        '''
        pass

    def stop(self):
        ''' stop actor 
        '''
        # stop child-actors
        for child in self.children:
            child.stop()
            
        try:
            self.on_stop()
        except:
            self._handle_failure(*sys.exc_info())
            
        self._processing = False
        #self._running = None

    def on_failure(self, exception_type, exception_value, traceback):
        ''' on failure event handler
        '''
        pass

    def _handle_message(self, message):
        ''' handle pyactors message
        
        returns True if the message is pyactors (system) message
        '''
        if not isinstance(message, dict):
            return False
        
        if message.get('system-msg', None):
            return True            
        return False

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
            try:
                message = self.inbox.get()
            except EmptyInboxException:
                message = None

            if message:
                try:
                    if not self._handle_message(message):
                        self.on_receive(message)
                except:
                    self._handle_failure(*sys.exc_info())
            
            try:    
                self.on_send()
            except:
                self._handle_failure(*sys.exc_info())
            yield
            
    def _supervise_loop(self):
        ''' supervise loop
        '''
        stopped_children = list()
        while self._processing:
            if self.children == 0:
                break
            # stopped_children = 0
            for child in self.children:
                if child.address not in stopped_children:
                    self.logger.debug('%s.supervise_loop(), child.run_once(): %s' % (self.name, child))
                    if not child.run_once():
                        stopped_children.append(child.address)
            if len(self.children) == len(stopped_children):
                self.logger.debug('%s.supervise_loop(), no active children (%s)' % (self.name, len(stopped_children)))
                break
            yield
    
    def run(self):
        ''' run actor 
        
        this method is used only when actor should be started as main one
        '''
        self.logger.debug('%s.run(), started' % self.name)
        try:
            self.on_start()
        except:
            self._handle_failure(*sys.exc_info())
            
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
                except:
                    self._handle_failure(*sys.exc_info())
            # supervise_loop        
            if supervise_loop is not None:
                self.logger.debug('%s.run(), supervising started' % self.name)
                try:
                    supervise_loop.next()
                    self.logger.debug('%s.run(), supervising on hold' % self.name)
                except StopIteration:
                    self.logger.debug('%s.run(), supervising completed' % self.name)
                    supervise_loop = None
                except:
                    self._handle_failure(*sys.exc_info())
            # exit if processing_loop and supervise_loop are None        
            if (processing_loop is None) and (supervise_loop is None):
                self.logger.debug('%s.run(), completed' % self.name)
                break
            yield True
        
        self.logger.debug('%s.run(), processing_loop completed' % self.name)
        self.logger.debug('%s.run(), supervise_loop completed' % self.name)
        yield False
        
    def run_once(self):
        ''' run actor once
        '''
        if self._running is not None:
            return self._running.next()
        else:
            return False
            
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

