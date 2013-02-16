import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest

import logging
_logger = logging.getLogger(__name__)

from pyactors.generator import GeneratorActor
from pyactors.thread import ThreadedGeneratorActor
from pyactors.exceptions import EmptyInboxException

from tests import TestGeneratorActor as TestActor
from tests import SenderGeneratorActor as SenderActor
from tests import ReceiverGeneratorActor as ReceiverActor

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
                if self.parent is not None:
                    self.parent.send(self.result)
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
            if self.parent is not None:
                self.parent.send(self.result)
            yield
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

    def test_actors_incorrect_processing_value_set(self):
        ''' test_actors_incorrect_processing_value_set
        '''
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_incorrect_processing_value_set' % __name__)
        actor = ThreadedActor()
        try:
            actor.processing = 1
        except RuntimeError:
            pass

    def test_actors_incorrect_waiting_value_set(self):
        ''' test_actors_incorrect_waiting_value_set
        '''
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_incorrect_waiting_value_set' % __name__)
        actor = ThreadedActor()
        try:
            actor.waiting = 1
        except RuntimeError:
            pass

    def test_actors_set_waiting_flag(self):
        ''' test_actors_set_waiting_flag
        '''
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_set_waiting_flag' % __name__)
        actor = ThreadedActor()
        actor.waiting = True
        self.assertEqual(actor.waiting, True)

    def test_actors_run(self):
        ''' test_threaded_actors.test_actors_run
        '''
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_run' % __name__)
        actor = ThreadedActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        self.assertEqual(actor.result, 45)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_stop_in_the_middle(self):
        ''' test_threaded_actors.test_actors_stop_in_the_middle
        '''  
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_stop_in_the_middle' % __name__)
        actor = LongRunningActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        time.sleep(0.1)
        actor.stop()
        self.assertGreater(actor.result, 0)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_processing_with_children(self):
        ''' test_threaded_actors.test_actors_processing_with_children
        '''    
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_processing_with_children' % __name__)
        parent = ThreadedActor()      
        for _ in range(5):
            parent.add_child(TestActor())      
        parent.start()
        while parent.processing:
            time.sleep(0.1)

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 50)

        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        
    def test_actors_processing_with_diff_timelife_children(self):
        ''' test_threaded_actors.test_actors_processing_with_diff_timelife_children
        '''    
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_processing_with_diff_timelife_children' % __name__)
        parent = ThreadedActor()      
        for i in range(5):
            parent.add_child(TestActor(iters=i))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(result, [0,0,0,0,1,1,1,3,3,6])
        self.assertEqual(len(result), 10)

        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        

    def test_actors_send_msg_between_actors(self):
        ''' test_threaded_actors.test_actors_send_msg_between_actors
        '''        
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_send_msg_between_actors' % __name__)
        parent = ThreadedActor()      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual(parent.inbox.get(), 'message from sender') 

    def test_actors_threaded_actor_in_actor(self):
        ''' test_threaded_actors.test_actors_threaded_actor_in_actor
        '''
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_threaded_actor_in_actor' % __name__)
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
        ''' test_threaded_actors.test_actors_send_msg_between_threaded_actors
        '''        
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_send_msg_between_threaded_actors' % __name__)
        parent = TestActor()      
        parent.add_child(ThreadedSenderActor(name='Sender'))      
        parent.add_child(ThreadedReceiverActor(name='Receiver'))      
        parent.start()
        parent.run()
        parent.stop()       
        self.assertEqual(
                [actor.message for actor in parent.find(actor_name='Receiver')],
                ['message from sender']
        ) 

    def test_actors_send_msg_between_threaded_actors_in_thread(self):
        ''' test_threaded_actors.test_actors_send_msg_between_threaded_actors in thread
        '''        
        logger = logging.getLogger('%s.ThreadedGeneratorActorTest.test_actors_send_msg_between_threaded_actors_in_thread' % __name__)
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
        
