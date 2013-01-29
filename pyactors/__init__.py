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
        self._name = name
        
        # actor address
        self.address = uuid.uuid4().hex
        
        # actor mailbox 
        self._mailbox = None
        
        # children dictionary
        self._children = dict()
        
        # used for checking if actor started or not
        self._started = False
        
        # postbox, used for sending messages to another actors
        self._postbox = None

    def __str__(self):
        ''' represent actor as string
        '''
        return u'%(class)s (%(address)s)' % {u'class': self.__class__.__name__, u'address': self.address }    

    def add_child(self, actor):
        ''' add actor's child
        '''
        if actor.address not in self.children:
            self._children[actor.address] = actor
        else:
            raise RuntimeError('Actor exists: %s', actor)

    def remove_child(self, address):
        ''' remove child by its address
        '''
        if actor.address in self.children:
            self._children.pop(actor.address)
        else:
            raise RuntimeError('Actor does not exist: %s', actor)
        
    @property
    def children(self):
        ''' return list of actor's children
        '''
        return self._children.values()

    def find(self, address=None, actor_class=None, actor_class_name=None):
        """ find children by criterias 
        
        - if no criterias are defined, return all children addresses
        
        - if `address` is defined as string or unicode, return an actor by its address.
        - if `address` is defined as list or tuple, return actors by thier addresses.
        
        - if actor_class is defined as string or unicode, return the list of all 
        existing actors of the given class, or of any subclass of the given class.
        - if actor_class is defined as list or tuple, return actors by thier actor classes.
        
        - if actor_class_name is defined, return the list of all existing actors of 
        the given class name.
        
        return existing actors by criterias.
        """
        if address and isinstance(address, (str, unicode)):
            return [actor for actor in self.children if actor.address == address]
            
        if address and isinstance(address, (list, tuple)):
            return [actor for actor in self.children if actor.address in address]
            
        if actor_class:
            return [actor for actor in self.children if isinstance(actor, actor_class)]
        
        if actor_class_name:
            return [actor for actor in self.children if actor.__class__.__name__ == actor_class_name]
        
        return self.children    

    @property
    def started(self):
        ''' return True if actor is started
        '''
        return self._started 

    def _supervise(self):
        ''' supervise child actors
        '''
        pass
        
    def run(self):
        ''' run actor
        '''
        pass

    def send(self, address, message):
        ''' send message to actor
        '''
        self._postbox.send(address, message)

    def sleep(self, timeout=0):
        ''' sleep actor for timeout
        '''
        pass        
    
class  ActorSystem(Actor):
    ''' Actor System
    '''
    pass
    
