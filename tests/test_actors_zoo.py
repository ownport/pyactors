import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest

import logging
_logger = logging.getLogger(__name__)

from pyactors.logs import file_logger
from pyactors.thread import ThreadedGeneratorActor
from pyactors.forked import ForkedGeneratorActor
from pyactors.forked import ForkedGreenletActor
from pyactors.exceptions import EmptyInboxException

from tests import TestGeneratorActor as ActorGe
from tests import TestGreenletActor as ActorGr

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
        test_name = 'test_actors_zoo.test_generator_and_greenlet'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = ActorGe(name='parent')
        parent.add_child(ActorGe(name='child-actor-ge-1'))
        parent.add_child(ActorGr(name='child-actor-gr-2'))
        parent.add_child(ActorGe(name='child-actor-ge-3'))
        parent.add_child(ActorGe(name='child-actor-ge-4'))
        parent.add_child(ActorGr(name='child-actor-gr-5'))
        parent.start()
        parent.run()
        parent.stop()
        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 50)
        
                
