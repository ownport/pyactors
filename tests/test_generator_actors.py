import sys
if '' not in sys.path:
    sys.path.append('')

import unittest

import pyactors
from pyactors.logs import file_logger
from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInboxException

from tests import ParentActor
from tests import SenderGeneratorActor as Sender
from tests import ReceiverGeneratorActor as Receiver
from tests import TestGeneratorActor as TestActor

def test_family():
    ''' test_generator_actors.test_family
    '''
    actor = TestActor()
    assert actor.family == pyactors.actor.AF_GENERATOR

def test_run():
    ''' test_generator_actors.test_run
    '''
    test_name = 'test_generator_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    actor = TestActor(name='Actor',logger=logger)
    actor.start()
    pyactors.joinall([actor,])

    result = []
    while True:
        try:
            result.append(actor.inbox.get())
        except EmptyInboxException:
            break
    assert len(result) == 10, result
    assert set(result) == set(['Actor:%d' % i for i in range(10)]), result

def test_processing_with_children():
    ''' test_generator_actors.test_processing_with_children
    '''    
    test_name = 'test_generator_actors.test_processing_with_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = TestActor(name='Parent', logger=logger, iters=3)      
    for i in range(5):
        parent.add_child(TestActor(name='Child-%s' % i, logger=logger, iters=3))      
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    
    assert len(result) == 18, result
    assert set(result) == set(['Parent:0','Parent:1','Parent:2',\
                               'Child-0:0','Child-0:1','Child-0:2', \
                               'Child-1:0','Child-1:1','Child-1:2', \
                               'Child-2:0','Child-2:1','Child-2:2', \
                               'Child-3:0','Child-3:1','Child-3:2', \
                               'Child-4:0','Child-4:1','Child-4:2',]), result

def test_processing_with_diff_timelife_children():
    ''' test_generator_actors.test_processing_with_diff_timelife_children
    '''    
    test_name = 'test_generator_actors.test_processing_with_diff_timelife_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = TestActor(name='Parent', logger=logger, iters=5)      
    for i in range(5):
        parent.add_child(TestActor(name='Child-%s' % i, logger=logger, iters=i))      
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    
    assert len(result) == 15, result
    assert set(result) == set(['Parent:0','Parent:1','Parent:2','Parent:3','Parent:4',\
                               'Child-1:0','Child-2:0','Child-2:1', \
                               'Child-3:0','Child-3:1','Child-3:2', \
                               'Child-4:0','Child-4:1','Child-4:2','Child-4:3',]), result

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
    assert parent.inbox.get() == 'message from sender'  

