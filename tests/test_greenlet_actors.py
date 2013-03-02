import sys
if '' not in sys.path:
    sys.path.append('')

import unittest

from pyactors.logs import file_logger
from pyactors.greenlet import GreenletActor
from pyactors.exceptions import EmptyInboxException

from tests import TestGreenletActor as TestActor
from tests import SenderGreenletActor as SenderActor
from tests import ReceiverGreenletActor as ReceiverActor

class GeventActorTest(unittest.TestCase):

    def test_run(self):
        ''' test_greenlet_actors.test_run
        '''
        test_name = 'test_greenlet_actors.test_run'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = TestActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        actor.run()

        result = []
        while True:
            try:
                result.append(actor.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 10)

        self.assertEqual(actor.run_once(), False)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_stop_in_the_middle(self):
        ''' test_greenlet_actors.test_stop_in_the_middle
        '''  
        test_name = 'test_greenlet_actors.test_stop_in_the_middle'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = TestActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        for _ in range(5):
            actor.run_once()
        actor.stop()

        result = []
        while True:
            try:
                result.append(actor.inbox.get())
            except EmptyInboxException:
                break
        self.assertGreater(len(result), 1)

        self.assertEqual(actor.run_once(), False)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_processing_with_children(self):
        ''' test_greenlet_actors.test_processing_with_children
        '''    
        test_name = 'test_greenlet_actors.test_processing_with_children'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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

    def test_processing_with_diff_timelife_children(self):
        ''' test_greenlet_actors.test_processing_with_diff_timelife_children
        '''    
        test_name = 'test_greenlet_actors.test_processing_with_diff_timelife_children'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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
        
    def test_send_msg_between_actors(self):
        ''' test_greenlet_actors.test_send_msg_between_actors
        '''        
        test_name = 'test_greenlet_actors.test_send_msg_between_actors'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = TestActor(name='ParentActor')      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        parent.run()
        parent.stop()       
        self.assertEqual(parent.inbox.get(), 'message from sender')

    def test_failed_actor(self):
        ''' test_greenlet_actors.test_failed_actor
        '''
        class FailedActor(GreenletActor):
            def loop(self):
                while True:
                    raise RuntimeError('Failed')
                    self.sleep()
        
        test_name = 'test_greenlet_actors.test_failed_actor'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = GreenletActor(logger=logger)
        parent.add_child(FailedActor(logger=logger))
        parent.start()
        parent.run()
        #self.assertRaises(RuntimeError, )


if __name__ == '__main__':
    unittest.main()
        
