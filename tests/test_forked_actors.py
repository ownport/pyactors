import sys
if '' not in sys.path:
    sys.path.append('')

import time
import logging
import unittest

from pyactors.generator import GeneratorActor
from pyactors.forked import ForkedGeneratorActor
from pyactors.forked import ForkedGreenletActor
from pyactors.exceptions import EmptyInboxException

_logger = logging.getLogger('test_forked_actors')

class ForkedGenActor(ForkedGeneratorActor):
    ''' Forked Generator Actor
    '''
    def __init__(self):
        super(ForkedGenActor, self).__init__()
        self.result = 0
    
    def loop(self):
        for i in xrange(10):
            if self.processing:
                self.result += i
                yield
            else:
                break
        self.stop()

class ForkedGreenActor(ForkedGreenletActor):
    ''' Forked Greenlet Actor
    '''
    def __init__(self):
        super(ForkedGreenActor, self).__init__()
        self.result = 0
    
    def loop(self):
        for i in xrange(10):
            if self.processing:
                self.result += i
                yield
            else:
                break
        self.stop()

class ForkedGeneratorActorTest(unittest.TestCase):

    def test_actors_run(self):
        ''' test_actors_run
        '''
        '''
        _logger.debug('ForkedGeneratorActorTest.test_actors_run()')
        actor = ForkedGenActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        self.assertEqual(actor.result, 45)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)
        '''
