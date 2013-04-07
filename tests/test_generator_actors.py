import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInbox

from tests import ParentGeneratorActor as ParentActor
from tests import SenderGeneratorActor as Sender
from tests import ReceiverGeneratorActor as Receiver
from tests import TestGeneratorActor as TestActor

def test_run():
    ''' test_generator_actors.test_run
    '''
    test_name = 'test_generator_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    actor = TestActor(name='Actor',logger=logger)
    actor.start()
    pyactors.joinall([actor,])

    storage_dump = actor.storage.dump()
    assert len(storage_dump) == 10, storage_dump
    assert set(storage_dump) == set(['Actor:%d' % i for i in range(10)]), storage_dump

def test_processing_with_children():
    ''' test_generator_actors.test_processing_with_children
    '''    
    test_name = 'test_generator_actors.test_processing_with_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent', logger=logger)      
    for i in range(5):
        parent.add_child(TestActor(name='Child-%s' % i, logger=logger, iters=3))      
    parent.start()
    pyactors.joinall([parent,])

    storage_dump = parent.storage.dump()
    assert len(storage_dump) == 15, storage_dump
    assert set(storage_dump) == set(['Child-0:0','Child-0:1','Child-0:2', \
                               'Child-1:0','Child-1:1','Child-1:2', \
                               'Child-2:0','Child-2:1','Child-2:2', \
                               'Child-3:0','Child-3:1','Child-3:2', \
                               'Child-4:0','Child-4:1','Child-4:2',]), storage_dump

def test_stop_children_in_the_middle():
    ''' test_generator_actors.test_stop_children_in_the_middle
    '''    
    class Parent(ParentActor):
        def on_handle(self):
            self.stop()
            
    test_name = 'test_generator_actors.test_stop_children_in_the_middle'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    
    parent = Parent(name='Parent', logger=logger)
    for i in range(5):
        parent.add_child(TestActor(name='Child-%s' % i, logger=logger, iters=3))      
    parent.start()
    pyactors.joinall([parent,])
    
    assert len(parent.storage) == 0, 'parent storage: %d' % len(parent.storage)

def test_processing_with_diff_timelife_children():
    ''' test_generator_actors.test_processing_with_diff_timelife_children
    '''    
    test_name = 'test_generator_actors.test_processing_with_diff_timelife_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent', logger=logger)      
    for i in range(5):
        parent.add_child(TestActor(name='Child-%s' % i, logger=logger, iters=i))      
    parent.start()
    pyactors.joinall([parent,])

    storage_dump = parent.storage.dump()
    assert len(storage_dump) == 10, storage_dump
    assert set(storage_dump) == set(['Child-1:0','Child-2:0','Child-2:1', \
                               'Child-3:0','Child-3:1','Child-3:2', \
                               'Child-4:0','Child-4:1','Child-4:2','Child-4:3',]), storage_dump

def test_send_msg_between_actors():
    ''' test_generator_actors.test_send_msg_between_actors
    '''        
    test_name = 'test_generator_actors.test_send_msg_between_actors'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent', logger=logger)      
    parent.add_child(Sender(name='Sender', logger=logger))      
    parent.add_child(Receiver(name='Receiver', logger=logger))      
    parent.start()
    pyactors.joinall([parent,])
    assert parent.storage.dump() == ['message from sender',]

def test_send_stop_msg_to_child():
    ''' test_generator_actors.test_send_stop_msg_to_child
    '''        
    class Parent(ParentActor):
        def on_handle(self):
        
            for child in self.children:
                self.logger.debug('%s.on_handle(), send "stop" message to child: %s' % (self.name, child))
                try:
                    child.send({'system-msg': {'type': 'stop', 'sender': self.address}})
                except:
                    pass
                
            if len(self.children) == 0:
                self.stop()
                
    test_name = 'test_generator_actors.test_send_stop_msg_to_child'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    parent = Parent(name='Parent', logger=logger)   
    for i in range(5):
        parent.add_child(TestActor(name='Child-%d' % i, logger=logger))
    parent.start()
    pyactors.joinall([parent,])
    
    assert len(parent.storage) > 0, 'storage: %s messages' % len(parent.storage)

def test_send_wrong_system_msg():
    ''' test_generator_actors.test_send_wrong_system_msg
    '''        
    class Parent(ParentActor):
        def on_handle(self):
            ''' on_handle
            '''
            for child in self.children:
                self.logger.debug('%s.on_handle(), send "wrong" system message to child: %s' % (self.name, child))
                try:
                    child.send({'system-msg': 'a1b2c3d4'})
                except:
                    self.logger.debug('%s.on_handle(), child stopped: %s' % (self.name, child))
                
            if len(self.children) == 0:
                self.stop()
                
        def on_receive(self, message):
            ''' on_receive
            '''
            self.logger.debug('%s.on_receive(), messages in inbox: %s' % (self.name, len(self.inbox)))
            self.logger.debug('%s.on_receive(), message: "%s" sent to storage' % (self.name, message))
            self.storage.put(message)
            self.logger.debug('%s.on_receive(), messages in storage: %d' % (self.name, len(self.storage)))
                
    test_name = 'test_generator_actors.test_send_wrong_system_msg'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    parent = Parent(name='Parent', logger=logger)      
    parent.add_child(TestActor(name='Child-0', logger=logger, iters=3))
    parent.start()
    pyactors.joinall([parent,])
    
    storage_dump = parent.storage.dump()
    assert len(storage_dump) == 3, 'parent storage: %s messages' % len(storage_dump)
    assert set(storage_dump) == set(['Child-0:0','Child-0:1','Child-0:2']), storage_dump


