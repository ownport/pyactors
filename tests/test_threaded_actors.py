import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest

from pyactors.logs import file_logger
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

    def test_incorrect_processing_value_set(self):
        ''' test_threaded_actors.test_incorrect_processing_value_set
        '''
        test_name = 'test_threaded_actors.test_incorrect_processing_value_set'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = ThreadedActor()
        try:
            actor.processing = 1
        except RuntimeError:
            pass

    def test_incorrect_waiting_value_set(self):
        ''' test_threaded_actors.test_incorrect_waiting_value_set
        '''
        test_name = 'test_threaded_actors.test_incorrect_waiting_value_set'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = ThreadedActor()
        try:
            actor.waiting = 1
        except RuntimeError:
            pass

    def test_set_waiting_flag(self):
        ''' test_threaded_actors.test_set_waiting_flag
        '''
        test_name = 'test_threaded_actors.test_set_waiting_flag'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = ThreadedActor()
        actor.waiting = True
        self.assertEqual(actor.waiting, True)

    def test_run(self):
        ''' test_threaded_actors.test_run
        '''
        test_name = 'test_threaded_actors.test_run'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = ThreadedActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        self.assertEqual(actor.result, 45)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_stop_in_the_middle(self):
        ''' test_threaded_actors.test_stop_in_the_middle
        '''  
        test_name = 'test_threaded_actors.test_stop_in_the_middle'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = LongRunningActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        time.sleep(0.1)
        actor.stop()
        self.assertGreater(actor.result, 0)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_processing_with_children(self):
        ''' test_threaded_actors.test_processing_with_children
        '''    
        test_name = 'test_threaded_actors.test_processing_with_children'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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
        
    def test_processing_with_diff_timelife_children(self):
        ''' test_threaded_actors.test_processing_with_diff_timelife_children
        '''    
        test_name = 'test_threaded_actors.test_processing_with_diff_timelife_children'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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
        

    def test_send_msg_between_actors(self):
        ''' test_threaded_actors.test_send_msg_between_actors
        '''        
        test_name = 'test_threaded_actors.test_send_msg_between_actors'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = ThreadedActor()      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual(parent.inbox.get(), 'message from sender') 

    def test_threaded_actor_in_actor(self):
        ''' test_threaded_actors.test_threaded_actor_in_actor
        '''
        test_name = 'test_threaded_actors.test_threaded_actor_in_actor'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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

    def test_send_msg_between_threaded_actors(self):
        ''' test_threaded_actors.test_send_msg_between_threaded_actors
        '''        
        test_name = 'test_threaded_actors.test_send_msg_between_threaded_actors'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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

    def test_send_msg_between_threaded_actors_in_thread(self):
        ''' test_threaded_actors.test_send_msg_between_threaded_actors_in_thread
        '''        
        test_name = 'test_threaded_actors.test_send_msg_between_threaded_actors_in_thread'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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
        
