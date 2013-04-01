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

from pyactors import PY3
from pyactors.inbox import GeventInbox
from pyactors.exceptions import EmptyInboxException

class NonBlockingIMap(object):
    ''' NonBlockingIMap class
    '''
    def __init__(self, func=None, in_queue=None, size=1, logger=None, nonstop=False, name=None):
        ''' __init__
        
        func        - greenlet function
        in_queue    - queue for incoming tasks
        size        - tasks pool size
        logger      - logger
        nonstop     - if True, no StopIteration exception
        '''
        if name is None:
            self._name = self.__class__.__name__
        else:
            self._name = name
        
        if size is not None and size <= 0:
            raise ValueError('size must not be negative and not equal zero: %r' % (size, ))
        self.size = size
        
        self.nonstop = nonstop
        
        if func is None:
            raise ValueError('func must be assigned: %s' % (func, ))
        self.func = func

        # greenlet counters
        self.count = 0        

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
    
    def __str__(self):
        return u'%s' % self.__class__.__name__

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
        
        self.logger.debug('%s, greenlets curr/max: %d/%d' % (self._name, self.count, self.size))

        if self.count >= self.size:
            return
        try:
            task = self._in_queue.get()
            self.logger.debug('%s, task from queue: %s' % (self._name, task))
            gevent.spawn(self.func, task).link(self._on_result)
            self.count += 1
        except EmptyInboxException:
            self.logger.debug('%s, empty incoming queue' % (self._name,))
            pass
            
        try:
            value = self._out_queue.get()
            self.logger.debug('%s, result value: %s' % (self._name, value))
        except EmptyInboxException:
            self.logger.debug('%s, empty outgoing queue' % (self._name,))
            pass
        
        if not self.nonstop and (not value and self.count <= 0):
            raise StopIteration()
        return value

    def _on_result(self, greenlet):
        ''' _on_result
        '''
        self.count -= 1
        if greenlet.successful():
            self._out_queue.put(greenlet.value)
        if greenlet.exception:
            self.logger.debug('%s, exception: %s' % (self._name, greenlet.exception))

def imap_nonblocking(func=None, in_queue=None, map_size=1, logger=None, nonstop=False, name=None):
    ''' The same as gevent.imap_unordered() except that process is non-blocking.
    '''
    return NonBlockingIMap(
                func=func, in_queue=in_queue, 
                size=map_size, logger=logger, 
                nonstop=nonstop, name=name)


