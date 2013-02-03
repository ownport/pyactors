import sys
if '' not in sys.path:
    sys.path.append('')

import time
import logging
import unittest

from pyactors.generator import GeneratorActor
from pyactors.thread import ThreadedGeneratorActor
from pyactors.exceptions import EmptyInboxException

_logger = logging.getLogger('test_threaded_actors')

class ThreadedActor(ThreadedGeneratorActor):
    ''' ThreadedActor
    '''
    def __init__(self):
        super(ThreadedActor, self).__init__()
        self.result = 0
    
    def loop(self):
        for i in xrange(10):
            if self.processing:
                self.result += i
                yield
            else:
                break
        self.stop()

class LongRunningActor(ThreadedGeneratorActor):
    ''' LongRunningActor
    '''
    def __init__(self):
        super(LongRunningActor, self).__init__()
        self.result = 0

    def loop(self):
        while self.processing:
        #for i in range(100):
            self.result += 1
            yield
        self.stop()

class TestActor(GeneratorActor):
    ''' TestActor
    '''
    def __init__(self, iters=10):
        super(TestActor, self).__init__()
        self.result = 0
        self.iters = iters
    
    def loop(self):
        for i in range(self.iters):
            if self.processing:
                self.result += i
                yield
            else:
                break
        self.stop()

class SenderActor(GeneratorActor):
    ''' Sender Actor
    '''
    def loop(self):
        for actor in self.find(actor_name='Receiver'):
            actor.send('message from sender')
        self.stop()

class ReceiverActor(GeneratorActor):
    ''' ReceiverActor
    '''
    def __init__(self, name=None):
        super(ReceiverActor, self).__init__(name=name)
        self.message = None
        
    def loop(self):
        while self.processing:
            try:
                self.message = self.inbox.get()    
            except EmptyInboxException:
                self.waiting = True
                yield
                
            if self.message:
                break
        self.stop()

class ThreadedSenderActor(ThreadedGeneratorActor):
    ''' Threaded Sender Actor
    '''
    def loop(self):
        for actor in self.find(actor_name='Receiver'):
            actor.send('message from sender')
        self.stop()

class ThreadedReceiverActor(ThreadedGeneratorActor):
    ''' Threaded Receiver Actor
    '''
    def __init__(self, name=None):
        super(ThreadedReceiverActor, self).__init__(name=name)
        self.message = None
        
    def loop(self):
        while self.processing:
            try:
                self.message = self.inbox.get()    
            except EmptyInboxException:
                self.waiting = True
                yield
                
            if self.message:
                break
        self.stop()

class ThreadedGeneratorActorTest(unittest.TestCase):

    def test_actors_run(self):
        ''' test_actors_run
        '''
        _logger.debug('ThreadedGeneratorActorTest.test_actors_run()')
        actor = ThreadedActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        self.assertEqual(actor.result, 45)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_stop_in_the_middle(self):
        ''' test_actors_stop_in_the_middle
        '''  
        _logger.debug('ThreadedGeneratorActorTest.test_actors_stop_in_the_middle')
        actor = LongRunningActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        time.sleep(0.1)
        actor.stop()
        self.assertGreater(actor.result, 0)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_processing_with_children(self):
        ''' test_actors_processing_with_children
        '''    
        _logger.debug('ThreadedGeneratorActorTest.test_actors_processing_with_children')
        parent = ThreadedActor()      
        for _ in range(5):
            parent.add_child(TestActor())      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        self.assertEqual([child.result for child in parent.children], [45,45,45,45,45])
        self.assertEqual(parent.run_once(), False)
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        
    def test_actors_processing_with_diff_timelife_children(self):
        ''' test_actors_processing_with_diff_timelife_children
        '''    
        _logger.debug('ThreadedGeneratorActorTest.test_actors_processing_with_diff_timelife_children')
        parent = ThreadedActor()      
        for i in range(5):
            parent.add_child(TestActor(iters=i))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        self.assertEqual(set([child.result for child in parent.children]), set([0,0,1,3,6]))
        self.assertEqual(parent.run_once(), False)
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        

    def test_actors_send_msg_between_actors(self):
        ''' test_actors_send_msg_between_actors
        '''        
        _logger.debug('ThreadedGeneratorActorTest.test_actors_send_msg_between_actors')
        parent = ThreadedActor()      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual(
                [actor.message for actor in parent.find(actor_name='Receiver')],
                ['message from sender']
        ) 

    def test_actors_threaded_actor_in_actor(self):
        ''' test_actors_threaded_actor_in_actor
        '''
        _logger.debug('ThreadedGeneratorActorTest.test_actors_threaded_actor_in_actor')
        parent = ThreadedActor()      
        parent.add_child(ThreadedActor())
        parent.add_child(ThreadedActor())      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual([child.result for child in parent.children], [45,45])
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)

    def test_actors_send_msg_between_threaded_actors(self):
        ''' test_actors_send_msg_between_threaded_actors
        '''        
        _logger.debug('ThreadedGeneratorActorTest.test_actors_send_msg_between_threaded_actors')
        parent = ThreadedActor()      
        parent.add_child(ThreadedSenderActor(name='Sender'))      
        parent.add_child(ThreadedReceiverActor(name='Receiver'))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual(
                [actor.message for actor in parent.find(actor_name='Receiver')],
                ['message from sender']
        ) 
        
