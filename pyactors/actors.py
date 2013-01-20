
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

import uuid
import logging

from pyactors.inbox import DequeInbox

_logger = logging.getLogger('pyactors')

''' Variables
'''
# Actor Status
class ActorStatus():
    ''' actor status '''
    not_started     = 0
    waiting         = 1
    processing      = 2
actor_status = ActorStatus()    


''' Exceptions
'''
class ActorDeadException(Exception):
    ''' Exception raised when trying to use a dead or unavailable actor
    '''
    pass

class NonRegisteredActorException(Exception):
    ''' Exception raised when trying to use a unregistered actor
    '''
    pass


''' Classes
'''

class Actor(object):
    ''' Actor
    '''
    def __init__(self, *args, **kwargs):
        ''' init
        '''
        # The actor URN string is a universally unique identifier for the actor.    
        self.urn = uuid.uuid4().urn
        
        # Actor's inbox
        self.inbox = DequeInbox()
        
        # postbox used for sending messages to another actors, 
        # assigned to actor when its registered in the environment
        self.postbox = None
        
        # actor processing loop
        self.running = self.loop()

    def __str__(self):
        ''' represent actor as string
        '''
        return "%(class)s (%(urn)s)" % {'class': self.__class__.__name__, 'urn': self.urn }

    def loop(self):
        ''' main actor's loop
        '''
        yield actor_status.not_started
        while True:
            yield actor_status.waiting

    def run_once(self):
        ''' run actor just once
        '''
        return self.running.next()
        
    def send(self, urn, message):
        ''' send message to another actors by urn
        '''
        if not isinstance(urn, (str, unicode)) and not urn.startswith('urn:uuid'):
            raise IncorrectURNException(urn)
        
        if not self.postbox:
            raise NonRegisteredActorException(self)
        self.postbox.send(urn, message)


class SimpleActor(Actor):
    ''' SimpleActor
    '''
    pass

