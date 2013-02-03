import sys
if '' not in sys.path:
    sys.path.append('')

import logging
import unittest

from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInboxException

_logger = logging.getLogger('test_generator_actors')


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

class Sender(GeneratorActor):
    ''' Sender
    '''
    def loop(self):
        for actor in self.find(actor_name='Receiver'):
            actor.send('message from sender')
        self.stop()

class Receiver(GeneratorActor):
    ''' Receiver
    '''
    def __init__(self, name=None):
        super(Receiver, self).__init__(name=name)
        self.message = None
        
    def loop(self):
        while self.processing:
            try:
                self.message = self.inbox.get()    
            except EmptyInboxException:
                self._waiting = True
                yield
                
            if self.message:
                break
        self.stop()


class GeneratorActorTest(unittest.TestCase):
    
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
        parent = GeneratorActor()      
        for _ in range(5):
            parent.add_child(TestActor())      
        parent.start()
        parent.run()
        self.assertEqual([child.result for child in parent.children], [45,45,45,45,45])
        self.assertEqual(parent.run_once(), False)
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        
    def test_actors_processing_with_diff_timelife_children(self):
        ''' test_actors_processing_with_diff_timelife_children
        '''    
        parent = GeneratorActor()      
        for i in range(5):
            parent.add_child(TestActor(iters=i))      
        parent.start()
        parent.run()
        self.assertEqual(set([child.result for child in parent.children]), set([0,0,1,3,6]))
        self.assertEqual(parent.run_once(), False)
        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        

    def test_actors_send_msg_between_actors(self):
        ''' test_actors_send_msg_between_actors
        '''        
        parent = GeneratorActor()      
        parent.add_child(Sender(name='Sender'))      
        parent.add_child(Receiver(name='Receiver'))      
        parent.start()
        parent.run()
        self.assertEqual(
                [actor.message for actor in parent.find(actor_name='Receiver')],
                ['message from sender']
        ) 








        
