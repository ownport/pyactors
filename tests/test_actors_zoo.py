import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest

import logging
_logger = logging.getLogger(__name__)

from pyactors.greenlet import GreenletActor
from pyactors.generator import GeneratorActor
from pyactors.thread import ThreadedGeneratorActor
from pyactors.forked import ForkedGeneratorActor
from pyactors.forked import ForkedGreenletActor
from pyactors.exceptions import EmptyInboxException

class ActorGe(GeneratorActor):
    ''' ActorGe
    '''
    def __init__(self, name=None, iters=10):
        super(ActorGe, self).__init__(name=name)
        self.result = 0
        self.iters = iters
    
    def loop(self):
        for i in range(self.iters):
            _logger.debug('%s.loop(), i/iters: %d/%d' % (self.name, i, self.iters))
            if self.processing:
                self.result += i
            else:
                break
            yield
        self.stop()
    
class ActorGr(GreenletActor):
    ''' ActorGr
    '''
    def __init__(self, name=None, iters=10):
        super(ActorGr, self).__init__(name=name)
        self.result = 0
        self.iters = iters
    
    def loop(self):
        for i in range(self.iters):
            _logger.debug('%s.loop(), i/iters: %d/%d' % (self.name, i, self.iters))
            if self.processing:
                self.result += i
            else:
                break
            self.sleep()
        self.stop()

class ActorTh(ThreadedGeneratorActor):
    pass 

class ActorFoGe(ForkedGeneratorActor):
    pass           

class ActorFoGr(ForkedGreenletActor):
    pass    

class ActorsZooTest(unittest.TestCase):
    
    def test_generator_and_greenlet(self):
        ''' test_actors_zoo.test_generator_and_greenlet
        '''
        parent = ActorGe(name='parent')
        parent.add_child(ActorGe(name='child-actor-ge-1'))
        parent.add_child(ActorGr(name='child-actor-gr-2'))
        parent.add_child(ActorGe(name='child-actor-ge-3'))
        parent.add_child(ActorGe(name='child-actor-ge-4'))
        parent.add_child(ActorGr(name='child-actor-gr-5'))
        parent.start()
        parent.run()
        parent.stop()
        self.assertEqual([child.result for child in parent.children], [45,45,45,45,45])
        
                
