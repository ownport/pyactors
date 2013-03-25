import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.greenlets import GeventInbox
from pyactors.exceptions import EmptyInboxException

from tests import TestGreenletActor as TestActor
from tests import ParentGeneratorActor as ParentActor
from tests import EchoClientGreenletActor as EchoClientActor
from tests import SenderGreenletActor as Sender
from tests import ReceiverGreenletActor as Receiver


from tests.settings import ECHO_SERVER_IP_ADDRESS
from tests.settings import ECHO_SERVER_IP_PORT


def test_family():
    ''' test_greenlet_actors.test_family
    '''
    actor = TestActor()
    assert actor.family == pyactors.actor.AF_GENERATOR

def test_run():
    ''' test_greenlet_actors.test_run
    '''
    test_name = 'test_greenlet_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent',logger=logger)
    child = TestActor(name='Child', logger=logger)
    parent.add_child(child)
    for i in range(10):
        child.send(test_name)
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    assert len(result) == 10, result
    assert result == ['imap_job:%s' % test_name for _ in range(10)], result

def test_echo_client():
    ''' test_greenlet_actors.test_echo_client
    '''
    test_name = 'test_greenlet_actors.test_echo_client'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent',logger=logger)
    child = EchoClientActor(name='EchoClientActor', logger=logger)
    parent.add_child(child)
    for _ in range(5):
        child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, test_name))
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    assert len(result) == 5, result
    assert result == ['imap_job:%s' % test_name for _ in range(5)], result

def test_echo_client_concurrent_requests():
    ''' test_greenlet_actors.test_echo_client_concurrent_requests
    '''
    test_name = 'test_greenlet_actors.test_echo_client_concurrent_requests'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent',logger=logger)
    child = EchoClientActor(name='EchoClientActor', logger=logger, imap_size=5)
    parent.add_child(child)
    for _ in range(20):
        child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, test_name))
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    assert len(result) == 20, result
    assert result == ['imap_job:%s' % test_name for _ in range(20)], result

def test_processing_with_children():
    ''' test_greenlet_actors.test_processing_with_children
    '''
    test_name = 'test_greenlet_actors.test_processing_with_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent', logger=logger)      
    for i in range(5):
        child = EchoClientActor(name='Child-%s' % i, logger=logger)
        for i in range(3):
            child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, '%s:%i' % (child.name, i)))
        parent.add_child(child)      
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    
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

    parent = ParentActor(name='Parent', logger=logger)      
    for i in range(5):
        child = EchoClientActor(name='Child-%s' % i, logger=logger)
        for ii in range(i):
            child.send((ECHO_SERVER_IP_ADDRESS, ECHO_SERVER_IP_PORT, '%s:%d' % (child.name, ii)))
        parent.add_child(child)      
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    
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

    parent = ParentActor(name='Parent', logger=logger)      
    parent.add_child(Sender(name='Sender', logger=logger))      
    parent.add_child(Receiver(name='Receiver', logger=logger))      
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
        child = TestActor(name='Child-%d' % i, logger=logger)
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
    child = TestActor(name='Child-0', logger=logger)
    for i in range(3):
        child.send('%s:%d' % (child.name, i))
    parent.add_child(child)
    parent.start()
    pyactors.joinall([parent,])
    
    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break

    assert len(result) == 3, 'parent.inbox: %s messages' % len(result)
    assert set(result) == set(['imap_job:Child-0:0','imap_job:Child-0:1','imap_job:Child-0:2']), result



    
