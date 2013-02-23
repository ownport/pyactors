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

from pyactors import AF_THREAD
from pyactors.generator import GeneratorActor

class ThreadedGeneratorActor(GeneratorActor):
    ''' Threaded GeneratorActor
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(ThreadedGeneratorActor,self).__init__(name=name, logger=logger)
        
        # Actor Family
        self._family = AF_THREAD
        
        self._processing = threading.Event()
        self._waiting = threading.Event()

        self._thread = threading.Thread(name=self._name, target=self.run)
        self._thread.daemon = True

    @property
    def processing(self):
        ''' return True if actor is processing 
        '''
        if self._processing.is_set():
            return True
        return False

    @processing.setter
    def processing(self, value):
        ''' set processing status 
        '''
        if not isinstance(value, bool):
            raise RuntimeError('Incorrect processing type, %s. It must be boolean' % value)
        if value:        
            self._processing.set()
        else:
            self._processing.clear()

    @property
    def waiting(self):
        ''' return True if actor is waiting for new messages
        '''
        if self._waiting.is_set():
            return True
        return False

    @waiting.setter
    def waiting(self, value):
        ''' set waiting status 
        '''
        if not isinstance(value, bool):
            raise RuntimeError('Incorrect waiting type, %s. It must be boolean' % value)
        if value:        
            self._waiting.set()
        else:
            self._waiting.clear()
                        
    def start(self):
        ''' start actor
        '''
        super(ThreadedGeneratorActor, self).start()
        
        self._thread.start()
    
        
