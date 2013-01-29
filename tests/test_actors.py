import sys
if '' not in sys.path:
    sys.path.append('')

import logging
import unittest
import pyactors

_logger = logging.getLogger('test_actors')


class ActorTest(unittest.TestCase):
    
    def test_actors_create(self):

        actor = pyactors.Actor()
        self.assertIsNotNone(actor)
        
