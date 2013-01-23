
__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__version__ = '0.1-gevent'
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

import gevent
import inspect

try:
    _basestring = basestring
except NameError:
    # Python 3
    _basestring = str

from pyactors.actors import Actor

__all__ = [
    'ActorSystem', 'actor_system', 
    'broadcast', 
    'find', 'get_by_class', 'get_by_class_name', 'get_by_urn', 
    'add', 'remove', 
    'run',
    'Actor',
]

#
#   logging
#
import logging
_logger = logging.getLogger('pyactors')

#
#   Exceptions
#
class IncorrectURNException(Exception):
    ''' Exception raised when trying to use URN different format than string or unicode
    '''
    pass

#
#   ActorSystem
#
class ActorSystem(object):
    ''' Actor System 
    '''
    
    def __init__(self):
        ''' __init__
        '''
        self._actors = dict()
    
    def add(self, actor):
        ''' add actor to the system
        '''
        if Actor not in inspect.getmro(actor.__class__):
            raise RuntimeError('Actor must be inherited from pyactors.Actor: %s' % actor)
        if actor.urn in self._actors:
            raise RuntimeError('Second attempt to add existing actor: %s' % actor)
            
        self._actors[actor.urn] = actor
        _logger.debug('Added %s', actor)
        return actor.urn

    def remove(self, urn):
        """ remove actor from the system.
        """
        if urn and urn in self._actors:
            self._actors.pop(urn)
            _logger.debug('Removed %s', urn)
        
        else:
            _logger.debug('Removing actor %s (not found in the system)', urn)
            raise RuntimeError('Actor not found in the system, urn: %s', urn)

    def find(self, urn=None, actor_class=None, actor_class_name=None):
        """ search actors in the system
        
        - if no criterias are defined, return all existing actors urn's
        
        - if urn is defined as string or unicode, return an actor by its URN.
        - if urn is defined as list or tuple, return actors by thier URNs.
        
        - if actor_class is defined as string or unicode, return the list of all 
        existing actors of the given class, or of any subclass of the given class.
        - if actor_class is defined as list or tuple, return actors by thier URNs.
        
        - if actor_class_name is defined, return the list of all existing actors of 
        the given class name.
        
        return existing actors by criterias.
        """
        if urn and isinstance(urn, (str, unicode)):
            return [actor for actor in self._actors.values() if actor.urn == urn]
        if urn and isinstance(urn, (list, tuple)):
            return [actor for actor in self._actors.values() if actor.urn in urn]
            
        if actor_class:
            return [actor for actor in self.find() if isinstance(actor, actor_class)]
        
        if actor_class_name:
            return [actor for actor in self.find() if actor.__class__.__name__ == actor_class_name]
        
        return self._actors.values()    

    def broadcast(self, message, target_class=None):
        ''' Broadcast message to all actors of the specified target_class.

        If no target_class is specified, the message is broadcasted to all
        actors.
        '''
        pass

    def run(self):
        ''' run actors in the system
        '''
        pass

    def stop_all(self, block=True, timeout=None):
        ''' Stop all running actors.

        block and timeout works as for Actor.stop().

        If block is True, the actors are guaranteed to be stopped
        in the reverse of the order they were started in. This is helpful if
        you have simple dependencies in between your actors, where it is
        sufficient to shut down actors in a LIFO manner: last started, first
        stopped.

        If you have more complex dependencies in between your actors, you
        should take care to shut them down in the required order yourself, e.g.
        by stopping dependees from a dependency's on_stop() method.
        '''
        pass

_actor_system = ActorSystem()

def add(actor):
    ''' add actor to the system
    '''
    return _actor_system.add(actor)

def remove(urn):
    ''' remove actor from the system
    '''
    _actor_system.remove(urn)

def find(urn=None, actor_class=None, actor_class_name=None):
    ''' return list of existing actors according to criterias
    
    see details in ActorSystem.find()
    '''
    return _actor_system.find(
                                urn=urn, 
                                actor_class=actor_class, 
                                actor_class_name=actor_class_name
    )

def broadcast(message, target_class=None):
    ''' Broadcast message to all actors of the specified target_class.
    '''
    _actor_system.broadcast(message, target_class)

def run():
    ''' Run initialized actors
    '''
    _actor_system.run()

    
