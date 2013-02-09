import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest

import logging
_logger = logging.getLogger(__name__)

from pyactors.forked import ForkedGreenletActor

from multiprocessing import Manager

class TestActor(ForkedGreenletActor):
    ''' Forked Greenlet Actor (test)
    '''
    def __init__(self):
        super(TestActor, self).__init__()
        self.result = Manager().Namespace()
        self.result.i = 0
    
    def loop(self):
        for i in xrange(10):
            if self.processing:
                self.result.i += i
                self.sleep()
            else:
                break
        self.stop()

class ForkedGreenletActorTest(unittest.TestCase):

    def test_actors_run(self):
        ''' test_forked_green_actors.test_actors_run
        '''
        _logger.debug('ForkedGreenletActorTest.test_actors_run()')
        actor = TestActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        actor.stop()
        self.assertEqual(actor.result.i, 45)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

if __name__ == '__main__':
    unittest.main()
