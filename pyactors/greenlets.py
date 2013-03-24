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

import gevent
import logging

from gevent.pool import Pool
from gevent.queue import Queue
from gevent.queue import Empty 
from gevent.greenlet import Greenlet

from pyactors import PY3
from pyactors.generator import GeneratorActor
from pyactors.inbox import EmptyInboxException

class GeventInbox(object):
    ''' Inbox from gevent.queue.Queue
    '''
    def __init__(self, logger=None):
        ''' __init__ 
        '''
        self.__inbox = Queue()
                    
        if logger is None:
            self._logger = logging.getLogger('%s.GeventInbox' % __name__)
        else:
            self._logger = logger

    def get(self):
        ''' get data from inbox 
        '''
        try:
            result = self.__inbox.get_nowait()
        except Empty:
            raise EmptyInboxException
        return result
    
    def put(self, message):
        ''' put message to inbox 
        '''
        self.__inbox.put_nowait(message)
    
    def __len__(self):
        ''' return length of inbox
        '''
        return self.__inbox.qsize()


class NonBlockingIMap(object):
    ''' NonBlockingIMap class
    '''
    def __init__(self, func=None, in_queue=None, size=1, logger=None, nonstop=False):
        ''' __init__
        
        func        - greenlet function
        in_queue    - queue for incoming tasks
        size        - tasks pool size
        logger      - logger
        nonstop     - if True, no StopIteration exception
        '''
        if size is not None and size <= 0:
            raise ValueError('size must not be negative and not equal zero: %r' % (size, ))
        self.size = size
        
        self.nonstop = nonstop
        
        if func is None:
            raise ValueError('func must be assigned: %s' % (func, ))
        self.func = func

        # greenlet counters
        self.greenlets_count = 0        

        # queues
        if in_queue is None:
            raise ValueError('in_queue must be assigned: %s' % (in_queue, ))
        self._in_queue = in_queue
        self._out_queue = GeventInbox()
        
        # logger
        if logger is None:
            self.logger = logging.getLogger('%s.Actor' % __name__)
        else:
            self.logger = logger

    def __iter__(self):
        ''' __iter__
        '''
        return self

    if PY3:
        __next__ = next
        del next

    def next(self):
        ''' next
        '''
        gevent.sleep()
        value = None
        
        self.logger.debug('%s, greenlets: %d' % (self, self.greenlets_count))
        self.logger.debug('%s, map size: %d' % (self, self.size))

        if self.greenlets_count >= self.size:
            return value
        try:
            self.logger.debug('%s, getting task' % self)
            task = self._in_queue.get()
            self.logger.debug('%s, task: %s' % (self, task))
            gevent.spawn(self.func, task).link(self._on_result)
            self.greenlets_count += 1
            self.logger.debug('%s, active greenlets: %d' % (self, self.greenlets_count))
        except EmptyInboxException:
            self.logger.debug('%s, empty incoming queue' % (self,))
            pass
            
        try:
            self.logger.debug('%s, getting value' % self)
            value = self._out_queue.get()
            self.logger.debug('%s, value: %s' % (self, value))
        except EmptyInboxException:
            self.logger.debug('%s, empty outgoing queue' % (self,))
            pass
        
        if not self.nonstop and (not value and self.greenlets_count <= 0):
            raise StopIteration()
        return value

    def _on_result(self, greenlet):
        ''' _on_result
        '''
        self.greenlets_count -= 1
        if greenlet.successful():
            self._out_queue.put(greenlet.value)

def imap_nonblocking(func=None, in_queue=None, map_size=1, logger=None, nonstop=False):
    ''' The same as gevent.imap_unordered() except that process is non-blocking.
    '''
    return NonBlockingIMap(func=func, in_queue=in_queue, size=map_size, logger=logger, nonstop=nonstop)


class GreenletActor(GeneratorActor):
    ''' GreenletActor
    '''
    @staticmethod
    def imap_job(message):
        ''' imap function for greenlets
        '''
        pass
    
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(GreenletActor, self).__init__(name=name, logger=logger)
        self.imap_queue = GeventInbox()

    def start(self, map_size=1):
        ''' start
        '''
        super(GreenletActor, self).start()
        self.imap = imap_nonblocking(
                                func=self.imap_job, in_queue=self.imap_queue, 
                                map_size=map_size, logger=self.logger,
                                nonstop=True)

