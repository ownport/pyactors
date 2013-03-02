__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__version__ = '0.3.0-new-design' 
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

import sys
import uuid
import logging

class Actor(object):
    ''' Base class for creating Actors 
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        # actor's name
        if not name:
            self._name = self.__class__.__name__
        else:
            self._name = name

        # actor address
        self.address = uuid.uuid4().hex

        if logger is None:
            self.logger = logging.getLogger('%s.Actor' % __name__)
        else:
            self.logger = logger

        # actor's inbox
        self.inbox = None
 
        # actor's parent
        self.parent = None

        # processing
        self._processing = False        

    def __str__(self):
        ''' represent actor as string
        '''
        return u'%(name)s[%(address)s]' % {u'name': self._name, u'address': self.address }    

    @property
    def name(self):
        ''' return actor name
        '''
        return self._name

    def on_start(self):
        ''' on start event handler
        '''
        pass

    def start(self):
        ''' start actor 
        '''
        self._processing = True

    def on_receive(self, message):
        ''' on receive message handler 
        '''
        pass

    def on_stop(self):
        ''' on stop event handler
        '''
        pass

    def stop(self):
        ''' stop actor 
        '''
        self._processing = False

    def on_failure(self, exception_type, exception_value, traceback):
        ''' on failure event handler
        '''
        pass

    def _handle_failure(self, exception_type, exception_value, traceback):
        ''' handle failure
        '''
        self.logger.error('Unhandled exception in %s' % self,
                           exc_info=(exception_type, exception_value, traceback))
        self.on_failure(exception_type, exception_value, traceback)
    
    def _processing_loop(self):
        ''' processing loop
        '''
        try:
            self.on_start()
        except Exception:
            self._handle_failure(*sys.exc_info())
            
        while self._processing:
            message = self.inbox.get()
            if message:
                self.on_receive(message)
            yield

        try:
            self.on_stop()
        except Exception:
            self._handle_failure(*sys.exc_info())
            
    def _supervise_loop(self):
        ''' supervise loop
        '''
        while self._processing:
            break
            yield
    
    def run(self):
        ''' run actor 
        
        this method is used only when actor should be started as main one
        '''
        processing_loop = self._processing_loop()
        supervise_loop = self._supervise_loop()
        while self._processing:
            if processing_loop:
                try:
                    processing_loop.next()
                except StopIteration:
                    processing_loop = None
                except Exception:
                    self._handle_failure(*sys.exc_info())
            if supervise_loop:
                try:
                    supervise_loop.next()
                except StopIteration:
                    supervise_loop = None
                except Exception:
                    self._handle_failure(*sys.exc_info())
            break

        
