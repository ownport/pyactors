import sys
if '' not in sys.path:
    sys.path.append('')

import logging
import unittest

from pyactors.greenlet import GreenletActor
from pyactors.exceptions import EmptyInboxException

_logger = logging.getLogger('test_gevent_actors')

class TestActor(GreenletActor):
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
                self.sleep()
            else:
                break
        self.stop()

class GeventActorTest(unittest.TestCase):

    def test_actors_run(self):
        ''' test_actors_run
        '''
        actor = TestActor()
        actor.start()
        self.assertEqual(actor.processing, True)
        actor.run()
        self.assertEqual(actor.result, 45)
        self.assertEqual(actor.run_once(), False)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_stop_in_the_middle(self):
        ''' test_actors_stop_in_the_middle
        '''  
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
        ''' test_actors_processing_with_children
        '''    
        parent = GreenletActor()      
        for _ in range(5):
            parent.add_child(TestActor())      
        parent.start()
        parent.run()
        self.assertEqual([child.result for child in parent.children], [45,45,45,45,45])
        self.assertEqual(parent.run_once(), False)
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)

    
