import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest

from pyactors.logs import file_logger
from pyactors.exceptions import EmptyInboxException

from tests import ForkedGreActor as TestActor

from multiprocessing import Manager

class ForkedGreenletActorTest(unittest.TestCase):

    def test_run(self):
        ''' test_forked_green_actors.test_run
        '''
        test_name = 'test_forked_gen_actors.test_run'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = TestActor()
        actor.start()
        while actor.processing:
            time.sleep(0.1)
        actor.stop()
        
        result = []
        while True:
            try:
                result.append(actor.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 10)

        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

if __name__ == '__main__':
    unittest.main()
