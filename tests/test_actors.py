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
        self.assertFalse(actor.started)
        self.assertIsNotNone(actor)

    def test_actors_address(self):

        actor = pyactors.Actor()
        self.assertNotEqual(actor.address, None)
        self.assertTrue(type(actor.address) == str)
        self.assertEqual(len(actor.address), 32)

