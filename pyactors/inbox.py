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

import Queue
import logging
import collections
import multiprocessing
from pyactors.exceptions import EmptyInboxException

class DequeInbox(object):
    ''' Inbox from collections.deque
    '''
    def __init__(self, logger=None):
        ''' __init__ 
        '''
        self.__inbox = collections.deque()
        if logger is None:
            self._logger = logging.getLogger('%s.DequeInbox' % __name__)
        else:
            self._logger = logger
                    
    def get(self):
        ''' get data from inbox 
        '''
        if len(self.__inbox) == 0:
            raise EmptyInboxException
        
        return self.__inbox.popleft()
    
    def put(self, message):
        ''' put message to inbox 
        '''
        self.__inbox.append(message)
    
    def __len__(self):
        ''' return length of inbox
        '''
        return len(self.__inbox)

class QueueInbox(object):
    ''' Inbox from Queue.Queue
    '''
    def __init__(self, logger=None):
        ''' __init__ 
        '''
        self.__inbox = Queue.Queue()
                    
        if logger is None:
            self._logger = logging.getLogger('%s.QueueInbox' % __name__)
        else:
            self._logger = logger

    def get(self):
        ''' get data from inbox 
        '''
        if self.__inbox.empty():
            raise EmptyInboxException
        
        return self.__inbox.get_nowait()
    
    def put(self, message):
        ''' put message to inbox 
        '''
        self.__inbox.put_nowait(message)
    
    def __len__(self):
        ''' return length of inbox
        '''
        return self.__inbox.qsize()

class ProcessInbox(object):
    ''' Inbox from multiprocessing.Queue
    '''
    def __init__(self, logger=None):
        ''' __init__ 
        '''
        self.__inbox = multiprocessing.Queue()
        
        if logger is None:
            self._logger = logging.getLogger('%s.ProcessInbox' % __name__)
        else:
            self._logger = logger

    def get(self):
        ''' get data from inbox 
        '''
        if self.__inbox.empty():
            raise EmptyInboxException
        
        return self.__inbox.get_nowait()
    
    def put(self, message):
        ''' put message to inbox 
        '''
        self.__inbox.put_nowait(message)
    
    def __len__(self):
        ''' return length of inbox
        '''
        return self.__inbox.qsize()

