__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__version__ = '0.1-concept'
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

try:
    import settings
except ImportError:
    pass    

class Actor(object):
    ''' Base class for creation actors
    '''
    def __init__(self, name=None):
        ''' __init__
        '''
        # actor name
        if not name:
            self._name = self.__class__.__name__
        else:
            self._name = name
        
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
        
    def __str__(self):
        ''' represent actor as string
        '''
        return u'%(name)s/%(address)s' % {u'name': self._name, u'address': self.address }    

    @property
    def waiting(self):
        ''' return True if actor is waiting for new messages
        '''
        return self._waiting

    @property
    def processing(self):
        ''' return True if actor is processing 
        '''
        return self._processing

    def add_child(self, actor):
        ''' add actor's child
        '''
        if actor.address not in self.children:
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
        children = list()
        
        if address and isinstance(address, (str, unicode)):
            children.extend([actor for actor in self.children if actor.address == address])
            if self.parent:
                children.extend(self.parent.find(address=address))
            return children
            
        if address and isinstance(address, (list, tuple)):
            children.extend([actor for actor in self.children if actor.address in address])
            if self.parent:
                children.extend(self.parent.find(address=address))
            return children
            
        if actor_class:
            children.extend([actor for actor in self.children if isinstance(actor, actor_class)])
            if self.parent:
                children.extend(self.parent.find(actor_class=actor_class))
            return children
        
        if actor_name:
            children.extend([actor for actor in self.children if actor._name == actor_name])
            if self.parent:
                children.extend(self.parent.find(actor_name=actor_name))
            return children
        
        return self.children.values()  
    
    def start(self):
        ''' start actor
        '''
        self._waiting = True
        self._processing = True
        if len(self.children) > 0:
            self.supervise()
        else:
            self.loop()

    def stop(self):
        ''' stop actor
        '''
        self._processing = False
        self._waiting = False

    def run(self):
        ''' run actor
        '''
        raise RuntimeError('Actor.run() is not implemented')
        
    def run_once(self):
        ''' run actor for one iteraction
        '''
        raise RuntimeError('Actor.run_once() is not implemented')

    def send(self, message):
        ''' send message to actor
        '''
        self.inbox.put(message)

    def loop(self):
        ''' mail loop 
        '''
        raise RuntimeError('Actor.loop() is not implemented')

    def supervise(self):
        ''' actor supervise
        '''
        raise RuntimeError('Actor.supervise() is not implemented')
            
class  ActorSystem(Actor):
    ''' Actor System
    '''
    pass
    
