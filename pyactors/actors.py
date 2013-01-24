
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

import uuid
import gevent
from gevent.queue import Queue

class Actor(gevent.Greenlet):
    ''' Actor
    '''
    def __init__(self):
        ''' __init__
        '''
        super(Actor, self).__init__()
        # The actor URN string is a universally unique identifier for the actor.    
        self.urn = uuid.uuid4().urn  
        # storage for incoming messages
        self.inbox = Queue()  
        # all messages send via postbox
        self.postbox = None
        
    def __str__(self):
        ''' represent actor as string
        '''
        return "%(class)s (%(urn)s)" % {'class': self.__class__.__name__, 'urn': self.urn }    

    def _run(self):
        ''' main loop
        '''
        while self.started:
            break

    def send(self, urn, message):
        ''' send message to another actors by urn
        '''
        if not isinstance(urn, (str, unicode)) and not urn.startswith('urn:uuid'):
            raise IncorrectURNException(urn)
        
        if not self.postbox:
            raise NonRegisteredActorException(self)
        self.postbox.send(urn, message)
            
