__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__version__ = '0.2.8'
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

import uuid
import logging

try:
    import settings
except ImportError:
    pass    

# Actor Family
AF_GENERATOR    = 0
AF_GREENLET     = 1
AF_THREAD       = 2
AF_PROCESS      = 3

class Actor(object):
    ''' Base class for creation actors
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        if logger is None:
            self.logger = logging.getLogger('%s.Actor' % __name__)
        else:
            self.logger = logger

        # actor name
        if not name:
            self._name = self.__class__.__name__
        else:
            self._name = name
        
        # actor family
        self._family = None
        
        # actor address
        self.address = uuid.uuid4().hex
        
        # actor's parent
        self.parent = None
        
        # actor inbox 
        self.inbox = None
        
        # children dictionary
        self._children = dict()
        
        # used for checking if actor is waiting messages or not
        self._waiting = False

        # used for checking if actor is processing 
        self._processing = False

        # actor processing loop 
        self.processing_loop = None
        
        # actor supervise loop
        self.supervise_loop = None
        
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
    def family(self):
        ''' return actor family
        '''
        if self._family is None:
            raise RuntimeError('Actor family is not specified, %s' % self._name)
        return self._family

    @property
    def waiting(self):
        ''' return True if actor is waiting for new messages
        '''
        return self._waiting

    @waiting.setter
    def waiting(self, value):
        ''' set waiting status 
        '''
        if isinstance(value, bool):
            self._waiting = value
        else:
            raise RuntimeError('Incorrect waiting type, %s. It must be boolean' % value)

    @property
    def processing(self):
        ''' return True if actor is processing 
        '''
        return self._processing

    @processing.setter
    def processing(self, value):
        ''' set processing status 
        '''
        if isinstance(value, bool):
            self._processing = value
        else:
            raise RuntimeError('Incorrect processing type, %s. It must be boolean' % value)

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
            self._children.pop(address)
        else:
            raise RuntimeError('Actor does not exist, address: %s', address)
        
    @property
    def children(self):
        ''' return list of actor's children
        '''
        return self._children.values()

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
    
    def start(self):
        ''' start actor
        '''
        self.waiting = False
        self.processing = True
        
        if len(self.children) > 0:
            # start child-actors
            for child in self.children:
                child.start()

    def _stop_children(self):
        ''' stop children
        '''
        if len(self.children) == 0:
            return
        # stop child-actors
        while True:
            stopped_children = 0
            for child in self.children:
                if child.processing:
                #if child.is_alive():
                    child.stop()
                else:
                    #self.remove_child(child.address)
                    stopped_children += 1
            if stopped_children == len(self.children):
                break

    def stop(self):
        ''' stop actor and its children
        '''
        self._stop_children()        
        self.processing = False
        self.waiting = False

    def run(self):
        ''' run actor
        '''
        raise RuntimeError('Actor.run() is not implemented')
        
    def run_once(self):
        ''' run actor for one iteraction (used by GeneratorActor and GreenletActor)
        '''
        raise RuntimeError('Actor.run_once() is not implemented')

    def send(self, message):
        ''' send message to actor
        '''
        self.inbox.put(message)

    def loop(self):
        ''' main loop 
        '''
        raise RuntimeError('Actor.loop() is not implemented')

    def supervise(self):        
        ''' supervise loop
        '''
        self.logger.debug('supervise started')
        while self.processing:
            stopped_children = 0
            for child in self.children:
                # child.processing is just a flag which give you information
                # that the actor should be stopped but it's not a fact
                # that the actor was stopped.
                if child.processing:
                #if child.is_alive():
                    if child.family in (AF_GENERATOR, AF_GREENLET):
                        try:
                            child.run_once()
                        except Exception, err:
                            self._logger.error(err)
                else:
                    stopped_children += 1
                yield

            if len(self.children) == stopped_children:
                break
        self.logger.debug('supervise stopped')
            
class  ActorSystem(Actor):
    ''' Actor System
    '''
    pass
    
