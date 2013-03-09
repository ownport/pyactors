import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.actor import Actor
from pyactors.logs import file_logger
from pyactors.exceptions import EmptyInboxException
from tests import SimpleActor

def test_actors_name():
    ''' test_actors.test_actors_name
    '''
    actor = SimpleActor()
    assert actor.name == 'SimpleActor'

    actor = SimpleActor(name='SimpleActor')
    assert actor.name == 'SimpleActor'

def test_actors_as_str():
    ''' test_actors.test_actors_as_str
    '''
    actor = SimpleActor()
    assert str(actor) == 'SimpleActor[%s]' % actor.address    

def test_actor_run():
    ''' test_actors.test_actor_run
    '''
    test_name = 'test_actors.test_actor_run'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    actor = SimpleActor(logger=logger)
    actor.start()
    pyactors.joinall([actor,])
    try:
        assert actor.inbox.get() == 'message-response'
    except EmptyInboxException:
        pass

def test_raise_error_on_start():
    ''' test_actors.test_raise_error_on_start
    '''
    class ErrorOnStartActor(SimpleActor):
        def on_start(self):
            self.logger.debug('on_start()')
            raise RuntimeError('Error on start')
                
    test_name = 'test_actors.test_raise_error_on_start'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    actor = ErrorOnStartActor(logger=logger)
    actor.start()
    pyactors.joinall([actor,])
    try:
        assert actor.inbox.get() == 'message-response'
    except EmptyInboxException:
        pass

def test_raise_error_on_stop():
    ''' test_actors.test_raise_error_on_stop
    '''
    class ErrorOnStopActor(SimpleActor):
        def on_stop(self):
            self.logger.debug('on_stop()')
            raise RuntimeError('Error on stop')
                
    test_name = 'test_actors.test_raise_error_on_stop'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    actor = ErrorOnStopActor(logger=logger)
    actor.start()
    pyactors.joinall([actor,])
    try:
        assert actor.inbox.get() == 'message-response'
    except EmptyInboxException:
        pass

def test_on_receive():
    ''' test_actors.test_on_receive
    '''
    class OnReceiveActor(Actor):
        def on_handle(self):
            self.stop()
            
    test_name = 'test_actors.test_on_receive'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    actor = OnReceiveActor(logger=logger)
    actor.send('message')
    actor.start()
    pyactors.joinall([actor,])
    try:
        assert actor.inbox.get() == 'message-response'
    except EmptyInboxException:
        pass
    
def test_on_receive_failure():
    ''' test_actors.test_on_receive_failure
    '''
    class OnReceiveFailureActor(Actor):
        def on_receive(self, message):
            raise RuntimeError('on receive failure')
            
    test_name = 'test_actors.test_on_receive_failure'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    actor = OnReceiveFailureActor(logger=logger)
    actor.send('message')
    actor.start()
    pyactors.joinall([actor,])
    try:
        assert actor.inbox.get() == 'message-response'
    except EmptyInboxException:
        pass
    
def test_on_handle_failure():    
    ''' test_actors.test_on_handle_failure
    '''
    class OnSendFailureActor(SimpleActor):
        def on_handle(self):
            raise RuntimeError('on send failure')
        
    test_name = 'test_actors.test_on_handle_failure'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    actor = OnSendFailureActor(logger=logger)
    actor.start()
    pyactors.joinall([actor,])
    try:
        assert actor.inbox.get() == 'message-response'
    except EmptyInboxException:
        pass

def test_add_remove_child():
    ''' test_actors.test_add_remove_child
    '''
    test_name = 'test_actors.test_add_remove_child'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    parent = Actor()
    parent.add_child(Actor())
    parent.add_child(Actor())
    parent.add_child(Actor())
    assert len(parent.children) == 3
        
    for actor in parent.children:
        parent.remove_child(actor.address)
    assert len(parent.children) == 0

def test_add_existing_actor():
    ''' test_add_existing_actor
    '''
    test_name = 'test_actors.test_add_existing_actor'
    logger = file_logger(name=test_name, filename='logs/%s.log' % test_name)

    parent = Actor()
    child = Actor()
    parent.add_child(child)
    try:
        parent.add_child(child)
        assert False
    except RuntimeError:
        pass

def test_remove_non_existing_actor():
    ''' test_remove_non_existing_actor
    '''
    test_name = 'test_actors.test_remove_non_existing_actor'        
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = Actor()
    child = Actor()
    try:
        parent.remove_child(child.address)
        assert False
    except RuntimeError:
        pass 

def test_find_children():
    ''' test_actors.test_find_children
    '''
    test_name = 'test_actors.test_find_children'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = Actor()
    child = Actor()
    parent.add_child(child)
    assert len(parent.find()) == 1
    parent.remove_child(child.address)
    assert len(parent.find()) == 0

def test_find_child_by_address():
    ''' test_actors.test_find_child_by_address
    '''
    test_name = 'test_actors.test_find_child_by_address'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = Actor()
    child = Actor()
    parent.add_child(child)
    assert len(parent.find(address=child.address)) == 1
    parent.remove_child(child.address)
    assert len(parent.find(address=child.address)) == 0
        
def test_find_child_by_address_list():
    ''' test_actors.test_find_child_by_address_list
    '''
    test_name = 'test_actors.test_find_child_by_address_list'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = Actor()
    children = [Actor() for _ in range(10)]
    addresses = list()
    for actor in children:
        addresses.append(actor.address)
        parent.add_child(actor)
    assert len(parent.find(address=addresses)) == 10
    for actor in children:
        parent.remove_child(actor.address)    
    assert len(parent.find(address=addresses)) == 0
            
def test_find_child_by_actor_class():
    ''' test_actors.test_find_child_by_actor_class
    '''
    test_name = 'test_actors.test_find_child_by_actor_class'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = Actor()
    child = Actor()
    parent.add_child(child)
    assert len(parent.find(actor_class=Actor)) == 1
    parent.remove_child(child.address)
    assert len(parent.find(actor_class=Actor)) == 0

def test_find_child_by_actor_name():
    ''' test_actors.test_find_child_by_actor_name
    '''
    test_name = 'test_actors.test_find_child_by_actor_name'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = Actor()
    child = Actor()
    parent.add_child(child)
    assert len(parent.find(actor_name='Actor')) == 1
    parent.remove_child(child.address)
    assert len(parent.find(actor_name='Actor')) == 0

    # name is defined        
    parent = Actor(name='Parent')
    child = Actor(name='Child')
    parent.add_child(child)
    assert len(parent.find(actor_name='Child')) == 1
    parent.remove_child(child.address)
    assert len(parent.find(actor_name='Child')) == 0

            
def test_find_child_by_actor_names():
    ''' test_actors.test_find_child_by_actor_names
    '''
    class TestActor(Actor):
        pass
        
    test_name = 'test_actors.test_child_by_actor_names'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = Actor()
    children = [TestActor() for _ in range(10)]
    for actor in children:
        parent.add_child(actor)
    assert len(parent.find(actor_name='TestActor')) == 10
    for actor in children:
        parent.remove_child(actor.address)    
    assert len(parent.find(actor_name='TestActor')) == 0
            
    # name is defined        
    parent = Actor(name='Parent')
    children = [TestActor(name='Child-TestActor') for _ in range(10)]
    for actor in children:
        parent.add_child(actor)
    assert len(parent.find(actor_name='Child-TestActor')) == 10
    for actor in children:
        parent.remove_child(actor.address)    
    assert len(parent.find(actor_name='Child-TestActor')) == 0

def test_find_childs_of_grandparents():
    ''' test_actors.test_find_childs_of_grandparents
    '''
    test_name = 'test_actors.test_find_childs_of_grandparents'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    grandparent = Actor(name='grandparent')
    for _ in range(3):
        grandparent.add_child(Actor(name='parent'))
    for parent in grandparent.children:
        for _ in range(2):
            parent.add_child(Actor(name='child'))            
    assert len(grandparent.children[0].children[0].find(actor_name='grandparent')) == 1
    assert len(grandparent.children[0].children[0].find(actor_name='parent')) == 3
    assert len(grandparent.children[0].children[0].find(actor_name='child')) == 2

