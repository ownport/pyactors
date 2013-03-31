import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInboxException
from pyactors.forked import ForkedGeneratorActor
from pyactors.inbox import ProcessInbox

from tests import ForkedParentActor


class TestForkedGeneratorActor(ForkedGeneratorActor):
    ''' TestForkedGeneratorActor
    '''
    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to parent: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_receive(), send "%s" to itself' % (self.name, message))
                self.send(message)
        
    def on_handle(self):
        ''' on_handle
        '''
        self.logger.debug('%s.on_handle()' % (self.name,))
        if len(self.inbox) == 0:
            self.stop()

class SenderForkedGeneratorActor(ForkedGeneratorActor):
    ''' SenderForkedGeneratorActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverForkedGeneratorActor(ForkedGeneratorActor):
    ''' ReceiverForkedGeneratorActor
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
    ''' test_forked_generator_actors.test_run
    '''
    test_name = 'test_forked_generator_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ForkedParentActor(name='Parent',logger=logger)
    child = TestForkedGeneratorActor(name='Child', logger=logger)
    parent.add_child(child)
    for i in range(10):
        child.send(test_name)
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 10, "len(result): %d, %s" % (len(result), result)
    assert result == [test_name for _ in range(10)], result

def test_processing_with_children():
    ''' test_forked_generator_actors.test_processing_with_children
    '''    
    test_name = 'test_forked_generator_actors.test_processing_with_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ForkedParentActor(name='Parent', logger=logger)      
    for i in range(5):
        child = TestForkedGeneratorActor(name='Child-%d' % i, logger=logger)
        parent.add_child(child)
        for ii in range(3):
            child.send('%s:%d' % (child.name, ii))
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 15, result
    assert set(result) == set(['Child-0:0','Child-0:1','Child-0:2', \
                               'Child-1:0','Child-1:1','Child-1:2', \
                               'Child-2:0','Child-2:1','Child-2:2', \
                               'Child-3:0','Child-3:1','Child-3:2', \
                               'Child-4:0','Child-4:1','Child-4:2',]), result

def test_stop_children_in_the_middle():
    ''' test_forked_generator_actors.test_stop_children_in_the_middle
    '''    
    class Parent(pyactors.actor.Actor):
        def __init__(self, name, logger):
            ''' __init__
            '''
            super(Parent, self).__init__(name=name, logger=logger)
            self.inbox = ProcessInbox()

        def on_handle(self):
            self.stop()
            
    test_name = 'test_forked_generator_actors.test_stop_children_in_the_middle'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    
    parent = Parent(name='Parent', logger=logger)
    for i in range(5):
        child = TestForkedGeneratorActor(name='Child-%d' % i, logger=logger)
        parent.add_child(child)
        for ii in range(100):
            child.send('%s:%d' % (child.name, ii))
    parent.start()
    pyactors.joinall([parent,])
    
    # Note: there's no concurrent behaviour for forked actors. As soon as 
    # forked actor is started, actor's processing started in the process and
    # parallel execution controlled by the system. In case of parent actor
    # sends stop message in the middle of execution, parent's inbox may
    # contains 0 messages or more but not more that final resul:
    # 5 children * 100 messages = 500
    #
    assert len(parent.inbox) >= 0 and len(parent.inbox) < 500, \
            'parent inbox size: %s' % len(parent.inbox)

def test_processing_with_diff_timelife_children():
    ''' test_forked_generator_actors.test_processing_with_diff_timelife_children
    '''    
    test_name = 'test_forked_generator_actors.test_processing_with_diff_timelife_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ForkedParentActor(name='Parent', logger=logger)      
    for i in range(5):
        child = TestForkedGeneratorActor(name='Child-%d' % i, logger=logger)
        parent.add_child(child)
        for ii in range(i):
            child.send('%s:%d' % (child.name, ii))
    parent.start()
    pyactors.joinall([parent,])

    result = parent.inbox.dump()
    assert len(result) == 10, result
    assert set(result) == set(['Child-1:0','Child-2:0','Child-2:1', \
                               'Child-3:0','Child-3:1','Child-3:2', \
                               'Child-4:0','Child-4:1','Child-4:2','Child-4:3',]), result

def test_send_msg_between_actors():
    ''' test_forked_generator_actors.test_send_msg_between_actors
    '''        
    test_name = 'test_forked_generator_actors.test_send_msg_between_actors'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ForkedParentActor(name='Parent', logger=logger)      
    parent.add_child(SenderForkedGeneratorActor(name='Sender', logger=logger))      
    parent.add_child(ReceiverForkedGeneratorActor(name='Receiver', logger=logger))      
    parent.start()
    pyactors.joinall([parent,])
    assert parent.inbox.dump() == ['message from sender',]

def test_send_stop_msg_to_child():
    ''' test_forked_generator_actors.test_send_stop_msg_to_child
    '''        
    class Parent(pyactors.actor.Actor):
        def __init__(self, name, logger):
            ''' __init__
            '''
            super(Parent, self).__init__(name=name, logger=logger)
            self.inbox = ProcessInbox()

        def on_handle(self):
        
            for child in self.children:
                self.logger.debug('%s.on_handle(), send "stop" message to child: %s' % (self.name, child))
                child.send({'system-msg': {'type': 'stop', 'sender': self.address}})
                
            if len(self.children) == 0:
                self.stop()
                
    test_name = 'test_forked_generator_actors.test_send_stop_msg_to_child'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    parent = Parent(name='Parent', logger=logger)      
    for i in range(5):
        child = TestForkedGeneratorActor(name='Child-%d' % i, logger=logger)
        parent.add_child(child)
        for ii in range(10):
            child.send('%s:%d' % (child.name, ii))
    parent.start()
    pyactors.joinall([parent,])
    
    assert len(parent.inbox) > 0, 'parent.inbox: %s messages' % len(parent.inbox)

def test_send_wrong_system_msg():
    ''' test_forked_generator_actors.test_send_wrong_system_msg
    '''        
    class Parent(pyactors.actor.Actor):
        def __init__(self, name, logger):
            ''' __init__
            '''
            super(Parent, self).__init__(name=name, logger=logger)
            self.inbox = ProcessInbox()

        def on_handle(self):
            ''' on_handle
            '''
            if len(self.children) == 0:
                self.stop()
                
        def on_receive(self, message):
            ''' on_receive
            '''
            self.logger.debug('%s.on_receive(), messages in inbox: %s' % (self.name, len(self.inbox)))
            self.send(message)
            self.logger.debug('%s.on_receive(), message: "%s" sent to itself' % (self.name, message))
                
    test_name = 'test_forked_generator_actors.test_send_wrong_system_msg'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    parent = Parent(name='Parent', logger=logger)      
    child = TestForkedGeneratorActor(name='Child-0', logger=logger)
    for i in range(3):
        child.send('%s:%d' % (child.name, i))

    logger.debug('%s.on_handle(), send "wrong" system message to child: %s' % (child.name, child))
    child.send({'system-msg': 'a1b2c3d4'})

    parent.add_child(child)
    parent.start()
    pyactors.joinall([parent,])
    
    result = parent.inbox.dump()
    assert len(result) == 3, 'parent.inbox: %s messages' % len(result)
    assert set(result) == set(['Child-0:0','Child-0:1','Child-0:2']), result


