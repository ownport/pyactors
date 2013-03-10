import sys
if '' not in sys.path:
    sys.path.append('')

import gevent
from gevent.queue import Queue

import pyactors

from pyactors.logs import file_logger
from pyactors.greenlets import imap_nonblocking

def simple_task(msg):
    return '%s:handled' % msg


def test_gevent_imap():
    ''' test_greenlets.test_gevent_imap
    '''
        
    queue = Queue()
    for i in range(5):
        queue.put('msg-%d' % i)
    imap = imap_nonblocking(3, simple_task, queue)        
    result = [msg for msg in imap if msg is not None]
    assert result == ['msg-0:handled','msg-1:handled','msg-2:handled',
                      'msg-3:handled','msg-4:handled',], result

def test_gevent_imap_zero_size():
    ''' test_greenlets.test_gevent_imap_zero_size
    '''
    try:
        imap = imap_nonblocking(0, simple_task, Queue())        
    except ValueError:
        pass

def test_gevent_imap_none_func():
    ''' test_greenlets.test_gevent_imap_none_func
    '''
    try:
        imap = imap_nonblocking(5, None, Queue())        
    except ValueError:
        pass

