import sys
if '' not in sys.path:
    sys.path.append('')

import time
import logging
import unittest

from pyactors.forked import ForkedGreenletActor
from pyactors.exceptions import EmptyInboxException

from multiprocessing import Manager

_logger = logging.getLogger('test_forked_actors')

class ForkedGreenActor(ForkedGreenletActor):
    ''' Forked Greenlet Actor
    '''
    def __init__(self):
        super(ForkedGreenActor, self).__init__()
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
        ''' test_actors_run
        '''
        _logger.debug('ForkedGreenletActorTest.test_actors_run()')
        actor = ForkedGreenActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        actor.stop()
        self.assertEqual(actor.result.i, 45)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

