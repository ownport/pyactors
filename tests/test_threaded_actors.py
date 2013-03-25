import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.exceptions import EmptyInboxException

from tests import ParentGeneratorActor as ParentActor
from tests import TestThreadedGeneratorActor as TestActor

def test_run():
    ''' test_threaded_actors.test_run
    '''
    test_name = 'test_threaded_actors.test_run'
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
    assert result == [test_name for _ in range(10)], result

def test_processing_with_children():
    ''' test_threaded_actors.test_processing_with_children
    '''    
    test_name = 'test_threaded_actors.test_processing_with_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent', logger=logger)      
    for i in range(5):
        child = TestActor(name='Child-%d' % i, logger=logger)
        parent.add_child(child)
        for ii in range(3):
            child.send('%s:%d' % (child.name, ii))
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    
    assert len(result) == 15, result
    assert set(result) == set(['Child-0:0','Child-0:1','Child-0:2', \
                               'Child-1:0','Child-1:1','Child-1:2', \
                               'Child-2:0','Child-2:1','Child-2:2', \
                               'Child-3:0','Child-3:1','Child-3:2', \
                               'Child-4:0','Child-4:1','Child-4:2',]), result

def test_stop_children_in_the_middle():
    ''' test_threaded_actors.test_stop_children_in_the_middle
    '''    
    class Parent(pyactors.actor.Actor):
        def on_handle(self):
            self.stop()
            
    test_name = 'test_threaded_actors.test_stop_children_in_the_middle'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 
    
    parent = Parent(name='Parent', logger=logger)
    for i in range(5):
        child = TestActor(name='Child-%d' % i, logger=logger)
        parent.add_child(child)
        for ii in range(10):
            child.send('%s:%d' % (child.name, ii))
    parent.start()
    pyactors.joinall([parent,])
    
    assert len(parent.inbox) == 0, 'parent inbox size: %s' % len(parent.inbox)

