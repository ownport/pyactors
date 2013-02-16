import sys
if '' not in sys.path:
    sys.path.append('')

import unittest
import logging
_logger = logging.getLogger(__name__)

from pyactors.exceptions import EmptyInboxException

from tests import TestGreenletActor as TestActor
from tests import SenderGreenletActor as SenderActor
from tests import ReceiverGreenletActor as ReceiverActor

class GeventActorTest(unittest.TestCase):

    def test_actors_run(self):
        ''' test_greenlet_actors.test_actors_run
        '''
        logger = logging.getLogger('%s.GeventActorTest.test_actors_run' % __name__)
        actor = TestActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        actor.run()
        self.assertEqual(actor.result, 45)
        self.assertEqual(actor.run_once(), False)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_stop_in_the_middle(self):
        ''' test_greenlet_actors.test_actors_stop_in_the_middle
        '''  
        logger = logging.getLogger('%s.GeventActorTest.test_actors_stop_in_the_middle' % __name__)
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
        ''' test_greenlet_actors.test_actors_processing_with_children
        '''    
        logger = logging.getLogger('%s.GeventActorTest.test_actors_processing_with_children' % __name__)
        parent = TestActor(name='ParentActor')      
        for i in range(5):
            parent.add_child(TestActor(name='ChildActor-%s' % i))      
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
        ''' test_greenlet_actors.test_actors_processing_with_diff_timelife_children
        '''    
        logger = logging.getLogger('%s.GeventActorTest.test_actors_processing_with_diff_timelife_children' % __name__)
        parent = TestActor(name='ParentActor')      
        for i in range(5):
            parent.add_child(TestActor(name='ChildActor-%i' % i, iters=i))      
        parent.start()
        parent.run()
        parent.stop()

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
        ''' test_greenlet_actors.test_actors_send_msg_between_actors
        '''        
        logger = logging.getLogger('%s.GeventActorTest.test_actors_send_msg_between_actors' % __name__)
        parent = TestActor(name='ParentActor')      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        parent.run()
        parent.stop()       
        self.assertEqual(
                [actor.message for actor in parent.find(actor_name='Receiver')],
                ['message from sender']
        ) 

if __name__ == '__main__':
    unittest.main()
        
