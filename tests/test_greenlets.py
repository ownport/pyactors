import sys
if '' not in sys.path:
    sys.path.append('')

import unittest
import pyactors

from pyactors.logs import file_logger

import gevent
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
    pass        
