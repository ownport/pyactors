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

import threading

from pyactors.inbox import QueueInbox
from pyactors.generator import GeneratorActor

class ThreadedGeneratorActor(GeneratorActor):
    ''' Threaded GeneratorActor
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(ThreadedGeneratorActor,self).__init__(name=name, logger=logger)
        
        self.inbox = QueueInbox()
        
        self._thread = threading.Thread(name=self._name, target=self.join)
        self._thread.daemon = True

    def start(self):
        ''' start 
        '''
        super(ThreadedGeneratorActor, self).start()
        self._thread.start()

    def join(self):
        ''' wait until actor finished
        '''
        while True:
            if self._running is None:
                break
            if not self._running.next():
                break
                
        self.stop()
        
