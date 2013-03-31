import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInboxException
from pyactors.inbox import ProcessInbox
from pyactors.forked import ForkedGreenletActor

from tests import ForkedParentActor
from tests.settings import ECHO_SERVER_IP_ADDRESS
from tests.settings import ECHO_SERVER_IP_PORT
from tests.echoclient import request_response


class TestForkedGreenletActor(ForkedGreenletActor):
    ''' TestForkedGreenletActor
    '''
    def __init__(self, name=None, logger=None):
        super(TestForkedGreenletActor, self).__init__(name=name, logger=logger)
        self.empty_msg_counter = 0
    
    @staticmethod
    def imap_job(message):
        return 'imap_job:%s' % message

    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to imap_queue: %s' % (self.name, message))
        self.imap_queue.put(message)
        self.logger.debug('%s.on_receive(), messages in imap_queue: %d' % (self.name, len(self.imap_queue)))
        
    def on_handle(self):
        ''' on_handle
        '''
        self.logger.debug('%s.on_handle()' % (self.name,))
        message = self.imap.next()
            
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_handle(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_handle(), send "%s" to itself' % (self.name, message))
                self.send(message)
        else:
            self.empty_msg_counter += 1
        
        if self.empty_msg_counter > 10:
            self.stop()
                    
class EchoClientGreenletActor(ForkedGreenletActor):
    ''' EchoClientGreenletActor
    '''
    @staticmethod
    def imap_job(message):
        host = message[0]
        port = message[1]
        return request_response(host, port, 'imap_job:%s\n' % message[2])
    
    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to imap queue: %s' % (self.name, message))
        self.imap_queue.put(message)

    def on_handle(self):
        ''' on_handle
        '''
        self.logger.debug('%s.on_handle()' % (self.name,))
        if len(self.inbox) == 0 and len(self.imap_queue) == 0 and self.imap.count == 0:            
            self.stop()

        message = self.imap.next()
        if message:
            message = message.strip()
            if self.parent is not None:
                self.logger.debug('%s.on_handle(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_handle(), send "%s" to itself' % (self.name, message))
                self.send(message)


class SenderGreenletActor(ForkedGreenletActor):
    ''' SenderGreenletActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverGreenletActor(ForkedGreenletActor):
    ''' ReceiverGreenletActor
    '''
    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_receive(), send "%s" to itself' % (self.name, message))
                self.send(message)
            self.stop()
    

''' 
-------------------------------------------
Tests
-------------------------------------------
'''
def test_run():
    ''' test_forked_greenlet_actors.test_run
    '''
    test_name = 'test_forked_greenlet_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ForkedParentActor(name='Parent',logger=logger)
    child = TestForkedGreenletActor(name='Child', logger=logger)
    parent.add_child(child)
    for i in range(10):
        child.send(test_name)
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 10, result
    assert result == ['imap_job:%s' % test_name for _ in range(10)], result

def test_echo_client():
    ''' test_forked_greenlet_actors.test_echo_client
    '''
    test_name = 'test_forked_greenlet_actors.test_echo_client'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ForkedParentActor(name='Parent',logger=logger)
    child = EchoClientGreenletActor(name='EchoClientActor', logger=logger)
    parent.add_child(child)
    for _ in range(5):
        child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, test_name))
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 5, result
    assert result == ['imap_job:%s' % test_name for _ in range(5)], result

def test_echo_client_concurrent_requests():
    ''' test_forked_greenlet_actors.test_echo_client_concurrent_requests
    '''
    test_name = 'test_forked_greenlet_actors.test_echo_client_concurrent_requests'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    total_msgs = 20

    parent = ForkedParentActor(name='Parent',logger=logger)
    child = EchoClientGreenletActor(name='EchoClientActor', logger=logger, imap_size=5)
    parent.add_child(child)
    for _ in range(total_msgs):
        child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, test_name))
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == total_msgs, result
    assert result == ['imap_job:%s' % test_name for _ in range(total_msgs)], result

