import sys
if '' not in sys.path:
    sys.path.append('')

import logging
_logger = logging.getLogger(__name__)

import unittest

from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInboxException

from tests import SenderGeneratorActor as Sender
from tests import ReceiverGeneratorActor as Receiver
from tests import TestGeneratorActor as TestActor

class GeneratorActorTest(unittest.TestCase):
    
    def test_actors_run(self):
        ''' test_generator_actors.test_actors_run
        '''
        logger = logging.getLogger('%s.GeneratorActorTest.test_actors_run' % __name__)
        actor = TestActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        actor.run()
        self.assertEqual(actor.result, 45)
        self.assertEqual(actor.run_once(), False)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_stop_in_the_middle(self):
        ''' test_generator_actors.test_actors_stop_in_the_middle
        '''  
        logger = logging.getLogger('%s.GeneratorActorTest.test_actors_stop_in_the_middle' % __name__)
        actor = TestActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        for _ in range(5):
            actor.run_once()
        actor.stop()
        self.assertEqual(actor.result, 10)
        self.assertEqual(actor.run_once(), False)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_processing_with_children(self):
        ''' test_generator_actors.test_actors_processing_with_children
        '''    
        logger = logging.getLogger('%s.GeneratorActorTest.test_actors_processing_with_children' % __name__)
        parent = GeneratorActor()      
        for _ in range(5):
            parent.add_child(TestActor())      
        parent.start()
        parent.run()

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 50)

        self.assertEqual(parent.run_once(), False)
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        
    def test_actors_processing_with_diff_timelife_children(self):
        ''' test_generator_actors.test_actors_processing_with_diff_timelife_children
        '''    
        logger = logging.getLogger('%s.GeneratorActorTest.test_actors_processing_with_diff_timelife_children' % __name__)
        parent = GeneratorActor()      
        for i in range(5):
            parent.add_child(TestActor(iters=i))      
        parent.start()
        parent.run()

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(result, [0,0,0,0,1,1,1,3,3,6])
        self.assertEqual(len(result), 10)

        self.assertEqual(parent.run_once(), False)
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        

    def test_actors_send_msg_between_actors(self):
        ''' test_generator_actors.test_actors_send_msg_between_actors
        '''        
        logger = logging.getLogger('%s.GeneratorActorTest.test_actors_send_msg_between_actors' % __name__)
        parent = GeneratorActor()      
        parent.add_child(Sender(name='Sender'))      
        parent.add_child(Receiver(name='Receiver'))      
        parent.start()
        parent.run()
        self.assertEqual(parent.inbox.get(), 'message from sender') 








        
