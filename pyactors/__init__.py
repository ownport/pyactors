
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
import logging

try:
    _basestring = basestring
except NameError:
    # Python 3
    _basestring = str

from pyactors.actors import Actor, SimpleActor

__all__ = [
    'ActorSystem', 'actor_system', 'broadcast', 'get_all', 'get_by_class',
    'get_by_class_name', 'get_by_urn', 'register', 'unregister', 'run',
    'Actor', 'SimpleActor',
]

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
        pass
    
    def register(self, actor):
        ''' register actor in the system
        '''
        pass

    def unregister(self, urn=None, actor=None):
        """ unregister actor from the system.
        """
        pass

    def get_all(self):
        """ return all running actors.
        """
        pass

    def get_by_urn(self, urn):
        ''' return an actor by its universally unique URN.
        '''
        pass

    def get_by_class(self, actor_class):
        ''' return the list of all running actors of the given class, or of
        any subclass of the given class.
        '''
        pass

    def get_by_class_name(self, actor_class_name):
        ''' return the list of all running actors of the given class
        name.
        '''
        pass

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

    
