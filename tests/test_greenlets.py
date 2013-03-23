import sys
if '' not in sys.path:
    sys.path.append('')

import gevent
import pyactors

from pyactors.logs import file_logger
from pyactors.greenlets import imap_nonblocking
from pyactors.greenlets import GeventInbox as Queue

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
    from gevent import socket
    from tests.settings import ECHO_SERVER_IP_ADDRESS
    from tests.settings import ECHO_SERVER_IP_PORT

    test_name = 'test_greenlets.test_echoclient'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    address = (ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT)
    out_msg = 'test_greenlets.test_echoclient\n'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    fileobj = sock.makefile()
    # send message
    fileobj.write(out_msg)
    fileobj.flush()
    # read message
    in_msg = fileobj.readline()
    if not in_msg:
        fileobj.close()
        assert False, 'empty message returned from echo server'
    fileobj.close()
    assert out_msg == in_msg, 'OUT: %s, IN: %s' % (out_msg, in_msg)
    
    
    
    
