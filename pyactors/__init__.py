
__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__version__ = '0.1'
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

import logging

from pyactors.inbox import DequeInbox, Postbox
from pyactors.actors import ActorDeadException
from pyactors.actors import Actor, SimpleActor
from pyactors.actors import actor_status

try:
    _basestring = basestring
except NameError:
    # Python 3
    _basestring = str

_logger = logging.getLogger('pyactors')

class IncorrectURNException(Exception):
    ''' Exception raised when trying to use URN different format than string or unicode
    '''
    pass


class ActorSystem(object):
    ''' Actor System 
    '''
    
    def __init__(self):
        ''' __init__
        '''
        # active actors
        self._actors_map = dict()
        # actor's inboxes
        self._inboxes = dict()
        # postbox for active actors
        self._postbox = Postbox(self._inboxes)
    
    def register(self, actor):
        ''' register actor in the system
        '''
        if not actor or not isinstance(actor, object):
            raise RuntimeError('Incorrect actor: %s' % actor)
        if actor.urn in self._actors_map:
            raise RuntimeError('Second attempt for actor registeration: %s' % actor)
            
        self._inboxes[actor.urn] = DequeInbox()
        actor.inbox = self._inboxes[actor.urn]
        actor.postbox = self._postbox
        self._actors_map[actor.urn] = actor
        _logger.debug('Registered %s', actor)
        return actor.urn

    def unregister(self, urn=None, actor=None):
        """ unregister actor from the system.
        """
        
        if actor and actor.urn in self._actors_map:
            self._actors_map.pop(actor.urn)
            self._inboxes.pop(actor.urn)
            _logger.debug('Unregistered %s', actor)
            
        elif urn and urn in  self._actors_map:
            self._actors_map.pop(urn)
            self._inboxes.pop(urn)
            _logger.debug('Unregistered %s', actor)
        
        else:
            _logger.debug('Unregistered %s (not found in the system)', actor)

    def get_all(self):
        """ return all running actors.
        """
        return self._actors_map.values()

    def get_by_urn(self, urn):
        ''' return an actor by its universally unique URN.
        '''
        if not isinstance(urn, (str, unicode)):
            raise IncorrectURNException(urn)
        if urn in self._actors_map:
            return actor[urn]
        return None

    def get_by_class(self, actor_class):
        ''' return the list of all running actors of the given class, or of
        any subclass of the given class.
        '''
        return [actor 
                    for actor in self.get_all() 
                    if isinstance(actor, actor_class)]

    def get_by_class_name(self, actor_class_name):
        ''' return the list of all running actors of the given class
        name.
        '''
        return [actor 
                    for actor in self.get_all() 
                    if actor.__class__.__name__ == actor_class_name]

    def broadcast(self, message, target_class=None):
        ''' Broadcast message to all actors of the specified target_class.

        If no target_class is specified, the message is broadcasted to all
        actors.
        '''
        if isinstance(target_class, _basestring):
            targets = self.get_by_class_name(target_class)
        elif target_class is not None:
            targets = self.get_by_class(target_class)
        else:
            targets = self.get_all()
        for actor in targets:
            self._postbox.send(actor.urn, message)

    def run(self):
        ''' run actors in the system
        '''
        total_actors = len(self._actors_map)
        stopped_actors = 0
        while True:
            if stopped_actors == total_actors:
                break
                
            # the number of waiting actors is 0 for every round 
            waiting_actors = 0
            
            for actor in self.get_all():
                try:
                    status = actor.run_once()

                    if status == actor_status.waiting:
                        waiting_actors += 1

                    elif status == actor_status.not_started:
                        self.unregister(actor=actor)
                        stopped_actors += 1
                        
                except StopIteration:
                    self.unregister(actor)
                    stopped_actors += 1
            
            # if all actors are waiting for data -> stop running
            if waiting_actors == total_actors:
                break

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

        # return [ref.stop(block, timeout) for ref in reversed(cls.get_all())]
        pass

actor_system = ActorSystem()

def register(actor):
    ''' register actor in the current system
    '''
    actor_system.register(actor)

def unregister(urn=None, actor=None):
    ''' unregister actor in the current system by URN or actor
    '''
    actor_system.unregister(urn, actor)

def get_all():
    ''' return list of active actors
    '''
    return actor_system.get_all()

def get_by_urn(urn):
    ''' return actor by URN
    '''
    return actor_system.get_by_urn(urn)

def get_by_class(actor_class):
    ''' return the list of actors selected by given class
    '''
    return actor_system.get_by_class(actor_class)

def get_by_class_name(actor_class_name):
    ''' return the list of actors selected by given class name
    '''
    return actor_system.get_by_class_name(actor_class_name)

def broadcast(message, target_class=None):
    ''' Broadcast message to all actors of the specified target_class.
    '''
    actor_system.broadcast(message, target_class)

def run():
    ''' Run initialized actors
    '''
    actor_system.run()

    
