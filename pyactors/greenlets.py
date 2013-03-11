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

from gevent.pool import Pool
from gevent.queue import Queue
from gevent.queue import Empty
from gevent.greenlet import Greenlet

from pyactors import PY3
from pyactors.actor import Actor
from pyactors.actor import AF_GENERATOR

class NonBlockingIMap(object):
    ''' NonBlockingIMap class
    '''
    def __init__(self, size=1, func=None, iterable=None):
        ''' __init__
        '''
        if size is not None and size <= 0:
            raise ValueError('size must not be negative and not equal zero: %r' % (size, ))
        self.size = size
        
        if func is None:
            raise ValueError('func must be assigned: %s' % (func, ))
        self.func = func

        self.greenlets_count = 0        
        self.iterable = iterable
        self.queue = Queue()

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
        if self.greenlets_count >= self.size:
            return value
        try:
            item = self.iterable.get_nowait()
            gevent.spawn(self.func, item).link(self._on_result)
            self.greenlets_count += 1
        except Empty:
            pass
            
        try:
            value = self.queue.get_nowait()
        except Empty:
            pass
            
        if not value and self.greenlets_count <= 0:
            raise StopIteration()
        return value

    def _on_result(self, greenlet):
        ''' _on_result
        '''
        self.greenlets_count -= 1
        if greenlet.successful():
            self.queue.put(greenlet.value)

def imap_nonblocking(map_size=2, func=None, iterable=None):
    ''' The same as gevent.imap_unordered() except that process is non-blocking.
    '''
    return NonBlockingIMap(size=map_size, func=func, iterable=iterable)


class GreenletActor(Actor):
    ''' Greenlet Actor
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(GreenletActor, self).__init__(name=name, logger=logger)
        
        # Actor Family
        self._family = AF_GENERATOR
                    
         
