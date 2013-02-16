import sys
if '' not in sys.path:
    sys.path.append('')

import unittest
import logging
_logger = logging.getLogger(__name__)

from pyactors.greenlet import GreenletActor
from pyactors.exceptions import EmptyInboxException


class TestActor(GreenletActor):
    ''' TestActor
    '''
    def __init__(self, name=None, iters=10):
        super(TestActor, self).__init__(name=name)
        self.result = 0
        self.iters = iters
    
    def loop(self):
        for i in range(self.iters):
            if self.processing:
                self.result += i
                if self.parent is not None:
                    self.parent.send(self.result)
            else:
                break
            self.sleep()
        self.stop()

class SenderActor(GreenletActor):
    ''' Sender Actor
    '''
    def loop(self):
        receiver_founded = False
        while self.processing:
            for actor in self.find(actor_name='Receiver'):
                actor.send('message from sender')
                receiver_founded = True
            if receiver_founded:
                break
        self.stop()

class ReceiverActor(GreenletActor):
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
                self._waiting = True
                
            if self.message:
                break
            
            self.sleep()
        self.stop()

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
        
