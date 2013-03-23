import sys
if '' not in sys.path:
    sys.path.append('')

import gevent
import pyactors

from pyactors.logs import file_logger
from pyactors.greenlets import imap_nonblocking
from pyactors.greenlets import GeventInbox as Queue

from tests.echoclient import request_response
from tests.settings import ECHO_SERVER_IP_ADDRESS
from tests.settings import ECHO_SERVER_IP_PORT

def simple_task(msg):
    return '%s:handled' % msg


def test_gevent_imap():
    ''' test_greenlets.test_gevent_imap
    '''
    test_name = 'test_greenlets.test_gevent_imap'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    queue = Queue()
    for i in range(5):
        queue.put('msg-%d' % i)
    logger.debug('in_queue: %s' % queue)
    imap = imap_nonblocking(simple_task, queue, 3, logger=logger)        
    logger.debug('imap: %s' % imap)
    result = [msg for msg in imap if msg is not None]
    logger.debug('result: %s' % result)
    assert result == ['msg-0:handled','msg-1:handled','msg-2:handled',
                      'msg-3:handled','msg-4:handled',], result

def test_gevent_imap_zero_size():
    ''' test_greenlets.test_gevent_imap_zero_size
    '''
    try:
        imap = imap_nonblocking(simple_task, Queue(), 0)        
    except ValueError:
        pass

def test_gevent_imap_none_func():
    ''' test_greenlets.test_gevent_imap_none_func
    '''
    try:
        imap = imap_nonblocking(None, Queue(), 5)        
    except ValueError:
        pass

def test_echoclient():
    ''' test_greenlets.test_echoclient
    '''
    test_name = 'test_greenlets.test_echoclient'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    out_msg = 'test_greenlets.test_echoclient\n'
    in_msg = request_response(ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, out_msg)
    assert out_msg == in_msg, 'OUT: %s, IN: %s' % (out_msg, in_msg)
        
def test_echoclient_pool():
    ''' test_greenlets.test_echoclient_pool
    '''
    test_name = 'test_greenlets.test_echoclient_pool'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    def check_result(greenlet):
        if greenlet.successful():
            assert greenlet.value.strip() == test_name, \
                    'wrong response from echo-server: "%s"' % greenlet.value
        else:
            assert False, 'Unsuccessful request_response, exception: %s' % greenlet.exception

    pool = gevent.pool.Pool(10)
    for i in range(100):
        pool.spawn(
                    request_response, 
                    ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, 
                    test_name + '\n').link(check_result)
    pool.join()

    
    
