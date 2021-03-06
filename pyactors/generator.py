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

from pyactors import Actor
from pyactors import AF_GENERATOR
from pyactors.inboxes import DequeInbox as Inbox

class GeneratorActor(Actor):
    ''' Generator Actor
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(GeneratorActor, self).__init__(name=name, logger=logger)
        
        # inbox
        self.inbox = Inbox()
        
        # Actor Family
        self._family = AF_GENERATOR

    def start(self):
        ''' start actor
        '''
        super(GeneratorActor, self).start()
        if len(self.children) > 0:
            self.supervise_loop = self.supervise()
        else:
            self.processing_loop = self.loop()

    def run_once(self):
        ''' one actor iteraction (processing + supervising)
        '''
        # processing
        if self.processing_loop:
            try:
                self.processing_loop.next()   
            except StopIteration:
                self.processing_loop = None
        # children supervising    
        if self.supervise_loop:
            try:
                self.supervise_loop.next()         
            except StopIteration:
                self.supervise_loop = None
                
        if self.processing_loop is not None or self.supervise_loop is not None:
            return True
        else:
            self.stop()
            return False

    def run(self):
        ''' run actor
        '''
        while self.processing:
            try:
                if not self.run_once():
                    break
            except Exception, err:
                self._logger(err)
                break
                    
                

        
                    
