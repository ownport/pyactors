import sys
if '' not in sys.path:
    sys.path.append('')

import unittest
import pyactors

from pyactors.logs import file_logger

import gevent
from gevent.pool import Pool
from gevent.queue import Queue
from gevent.queue import Empty

def test_greenlet_wrapper():
    ''' test_greenlets.test_greenlet_wrapper
    '''
    
    def func():
        gevent.sleep(0)
    
    gevent.spawn(func)

def test_greenlet_pool():
    ''' test_greenlets.test_greenlet_pool
    '''
    def task(message):
        return '%s-handled' % message
    
    pool = Pool(3)
    for r in pool.imap_unordered(task, range(10)):
        print r
    assert True

def test_greenlet_pool_queue():
    ''' test_greenlets.test_greenlet_pool_queue
    '''
    def task(queues):
        in_queue, out_queue = queues
        try:
            msg = in_queue.get_nowait()
        except Empty:
            return
        out_queue.put_nowait('%s-handled' % msg)
    
    in_queue = Queue()
    out_queue = Queue()
    for i in range(10):
        in_queue.put_nowait('msg-%d' % i)
    
    pool = Pool(5)
    while True:
        gevent.sleep(0)
        pool.spawn(task, (in_queue,out_queue))
        try:
            print out_queue.get_nowait()
        except Empty:
            break
    assert True
