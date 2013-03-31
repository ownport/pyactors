import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.greenlet import GeventInbox
from pyactors.greenlet import GreenletActor
from pyactors.exceptions import EmptyInboxException

from tests import ParentGeneratorActor
from tests.settings import ECHO_SERVER_IP_ADDRESS
from tests.settings import ECHO_SERVER_IP_PORT
from tests.echoclient import request_response


class TestGreenletActor(GreenletActor):
    ''' TestGreenletActor
    '''
    def __init__(self, name=None, logger=None):
        super(TestGreenletActor, self).__init__(name=name, logger=logger)
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
                    
class EchoClientGreenletActor(GreenletActor):
    ''' EchoClientGreenletActor
    '''
    @staticmethod
    def imap_job(message):
        return request_response(message[0], message[1], 'imap_job:%s\n' % message[2])
    
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


class SenderGreenletActor(GreenletActor):
    ''' SenderGreenletActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverGreenletActor(GreenletActor):
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
Tests
'''

def test_run():
    ''' test_greenlet_actors.test_run
    '''
    test_name = 'test_greenlet_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentGeneratorActor(name='Parent',logger=logger)
    child = TestGreenletActor(name='Child', logger=logger)
    parent.add_child(child)
    for i in range(10):
        child.send(test_name)
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 10, result
    assert result == ['imap_job:%s' % test_name for _ in range(10)], result

def test_echo_client():
    ''' test_greenlet_actors.test_echo_client
    '''
    test_name = 'test_greenlet_actors.test_echo_client'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentGeneratorActor(name='Parent',logger=logger)
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
    ''' test_greenlet_actors.test_echo_client_concurrent_requests
    '''
    test_name = 'test_greenlet_actors.test_echo_client_concurrent_requests'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentGeneratorActor(name='Parent',logger=logger)
    child = EchoClientGreenletActor(name='EchoClientActor', logger=logger, imap_size=5)
    parent.add_child(child)
    for _ in range(20):
        child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, test_name))
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 20, result
    assert result == ['imap_job:%s' % test_name for _ in range(20)], result

def test_processing_with_children():
    ''' test_greenlet_actors.test_processing_with_children
    '''
    test_name = 'test_greenlet_actors.test_processing_with_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentGeneratorActor(name='Parent', logger=logger)      
    for i in range(5):
        child = EchoClientGreenletActor(name='Child-%s' % i, logger=logger)
        for i in range(3):
            child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, '%s:%i' % (child.name, i)))
        parent.add_child(child)      
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 15, result
    assert set(result) == set(['imap_job:Child-0:0','imap_job:Child-0:1','imap_job:Child-0:2', \
                               'imap_job:Child-1:0','imap_job:Child-1:1','imap_job:Child-1:2', \
                               'imap_job:Child-2:0','imap_job:Child-2:1','imap_job:Child-2:2', \
                               'imap_job:Child-3:0','imap_job:Child-3:1','imap_job:Child-3:2', \
                               'imap_job:Child-4:0','imap_job:Child-4:1','imap_job:Child-4:2',]), result

def test_processing_with_diff_timelife_children():
    ''' test_greenlet_actors.test_processing_with_diff_timelife_children
    '''
    test_name = 'test_greenlet_actors.test_processing_with_diff_timelife_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentGeneratorActor(name='Parent', logger=logger)      
    for i in range(5):
        child = EchoClientGreenletActor(name='Child-%s' % i, logger=logger)
        for ii in range(i):
            child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, '%s:%d' % (child.name, ii)))
        parent.add_child(child)      
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 10, result
    assert set(result) == set(['imap_job:Child-1:0','imap_job:Child-2:0','imap_job:Child-2:1', \
                               'imap_job:Child-3:0','imap_job:Child-3:1','imap_job:Child-3:2', \
                               'imap_job:Child-4:0','imap_job:Child-4:1','imap_job:Child-4:2', \
                               'imap_job:Child-4:3',]), result

def test_send_msg_between_actors():
    ''' test_greenlet_actors.test_send_msg_between_actors
    '''        
    test_name = 'test_greenlet_actors.test_send_msg_between_actors'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentGeneratorActor(name='Parent', logger=logger)      
    parent.add_child(SenderGreenletActor(name='Sender', logger=logger))      
    parent.add_child(ReceiverGreenletActor(name='Receiver', logger=logger))      
    parent.start()
    pyactors.joinall([parent,])
    assert parent.inbox.get() == 'message from sender'  

def test_send_stop_msg_to_child():
    ''' test_greenlet_actors.test_send_stop_msg_to_child
    '''        
    class Parent(pyactors.actor.Actor):
        def on_handle(self):
        
            for child in self.children:
                self.logger.debug('%s.on_handle(), send "stop" message to child: %s' % (self.name, child))
                child.send({'system-msg': {'type': 'stop', 'sender': self.address}})
                
            if len(self.children) == 0:
                self.stop()
                
    test_name = 'test_greenlet_actors.test_send_stop_msg_to_child'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    parent = Parent(name='Parent', logger=logger)      
    for i in range(5):
        child = TestGreenletActor(name='Child-%d' % i, logger=logger)
        for i in range(3):
            child.send(test_name)
        parent.add_child(child)
    parent.start()
    pyactors.joinall([parent,])
    
    assert len(parent.inbox) > 0, 'parent.inbox: %s messages' % len(parent.inbox)

def test_send_wrong_system_msg():
    ''' test_greenlet_actors.test_send_wrong_system_msg
    '''        
    class Parent(pyactors.actor.Actor):
        def on_handle(self):
            ''' on_handle
            '''
            for child in self.children:
                self.logger.debug('%s.on_handle(), send "wrong" system message to child: %s' % (self.name, child))
                child.send({'system-msg': 'a1b2c3d4'})
                
            if len(self.children) == 0:
                self.stop()
                
        def on_receive(self, message):
            ''' on_receive
            '''
            self.logger.debug('%s.on_receive(), messages in inbox: %s' % (self.name, len(self.inbox)))
            self.send(message)
            self.logger.debug('%s.on_receive(), message: "%s" sent to itself' % (self.name, message))
                
    test_name = 'test_greenlet_actors.test_send_wrong_system_msg'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    parent = Parent(name='Parent', logger=logger)      
    child = TestGreenletActor(name='Child-0', logger=logger)
    for i in range(3):
        child.send('%s:%d' % (child.name, i))
    parent.add_child(child)
    parent.start()
    pyactors.joinall([parent,])
    
    result = parent.inbox.dump()
    assert len(result) == 3, 'parent.inbox: %s messages' % len(result)
    assert set(result) == set(['imap_job:Child-0:0','imap_job:Child-0:1','imap_job:Child-0:2']), result

