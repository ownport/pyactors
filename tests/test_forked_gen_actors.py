import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest
import logging
_logger = logging.getLogger(__name__)

from pyactors.generator import GeneratorActor
from pyactors.forked import ForkedGeneratorActor
from pyactors.exceptions import EmptyInboxException

from multiprocessing import Manager


class TestActor(GeneratorActor):
    ''' TestActor
    '''
    def __init__(self, name=None, iters=10):
        super(TestActor, self).__init__(name=name)
        self.result = Manager().Namespace()
        self.result.i = 0
        self.iters = iters
    
    def loop(self):
        for i in range(self.iters):
            if self.processing:
                self.result.i += i
                yield
            else:
                break
        self.stop()
        
class ForkedGenActor(ForkedGeneratorActor):
    ''' Forked Generator Actor
    '''
    def __init__(self, name=None):
        super(ForkedGenActor, self).__init__(name=name)
        self.result = Manager().Namespace()
        self.result.i = 0
    
    def loop(self):
        for i in xrange(10):
            if self.processing:
                self.result.i += i
                yield
            else:
                break
        self.stop()

class LongRunningActor(ForkedGeneratorActor):
    ''' LongRunningActor
    '''
    def __init__(self, name=None):
        super(LongRunningActor, self).__init__(name=name)
        self.result = Manager().Namespace()
        self.result.i = 0

    def loop(self):
        while self.processing:
        #for i in range(100):
            self.result.i += 1
            yield
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
        self.result = Manager().Namespace()
        self.result.message = None
        
    def loop(self):
        while self.processing:
            try:
                self.result.message = self.inbox.get()    
            except EmptyInboxException:
                self.waiting = True
                yield
                
            if self.result.message:
                break
        self.stop()

class ForkedGeneratorActorTest(unittest.TestCase):

    def test_actors_run(self):
        ''' test_forked_gen_actors.test_actors_run
        '''
        _logger.debug('ForkedGeneratorActorTest.test_actors_run()')
        actor = ForkedGenActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        actor.stop()
        self.assertEqual(actor.result.i, 45)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_stop_in_the_middle(self):
        ''' test_forked_gen_actors.test_actors_stop_in_the_middle
        '''  
        _logger.debug('ForkedGeneratorActorTest.test_actors_stop_in_the_middle')
        actor = LongRunningActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        time.sleep(0.1)
        actor.stop()
        self.assertGreater(actor.result.i, 0)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_processing_with_children(self):
        ''' test_forked_gen_actors.test_actors_processing_with_children
        '''    
        _logger.debug('ForkedGeneratorActorTest.test_actors_processing_with_children')
        parent = ForkedGenActor()      
        for _ in range(5):
            parent.add_child(TestActor())      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()
        self.assertEqual([child.result.i for child in parent.children], [45,45,45,45,45])
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        
    def test_actors_processing_with_diff_timelife_children(self):
        ''' test_forked_gen_actors.test_actors_processing_with_diff_timelife_children
        '''    
        _logger.debug('ForkedGeneratorActorTest.test_actors_processing_with_diff_timelife_children')
        parent = ForkedGenActor()      
        for i in range(5):
            parent.add_child(TestActor(iters=i))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()
        self.assertEqual(set([child.result.i for child in parent.children]), set([0,0,1,3,6]))
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        

    def test_actors_send_msg_between_actors(self):
        ''' test_forked_gen_actors.test_actors_send_msg_between_actors
        '''        
        _logger.debug('ForkedGeneratorActorTest.test_actors_send_msg_between_actors')
        parent = ForkedGenActor()      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual(
                [actor.result.message for actor in parent.find(actor_name='Receiver')],
                ['message from sender']
        ) 

    def test_actors_forked_actor_in_actor(self):
        ''' test_forked_gen_actors.test_actors_forked_actor_in_actor
        '''
        _logger.debug('ForkedGeneratorActorTest.test_actors_forked_actor_in_actor')
        parent = ForkedGenActor()      
        parent.add_child(ForkedGenActor())
        parent.add_child(ForkedGenActor())      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual([child.result.i for child in parent.children], [45,45])
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)

    def test_actors_send_msg_between_forked_actors(self):
        ''' test_forked_gen_actors.test_actors_send_msg_between_forked_actors
        '''        
        _logger.debug('ForkedGeneratorActorTest.test_actors_send_msg_between_forked_actors')
        # TODO
        '''
        parent = ForkedGenActor(name='ForkedSenderReceiver')      
        parent.add_child(ForkedSenderActor(name='ForkedSender'))      
        parent.add_child(ForkedReceiverActor(name='ForkedReceiver'))      
        parent.start()
        time_start = time.time()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        '''

