import sys
if '' not in sys.path:
    sys.path.append('')

import logging
import unittest
import pyactors

_logger = logging.getLogger('test_actors')

class ActorTest(unittest.TestCase):
    
    def test_actor_urn(self):
        ''' test actor URN
        '''
        a1 = pyactors.Actor()
        self.assertTrue(a1.urn.startswith('urn:uuid:'))

    def test_actor_as_str(self):
        ''' test represent actor as string
        '''
        a1 = pyactors.Actor()
        self.assertTrue(str(a1).startswith('Actor (urn:uuid:'))

    def test_actor_states(self):
        ''' check actor states
        '''
        a1 = pyactors.Actor()

        # initial states
        self.assertEqual(a1.started, False)
        self.assertEqual(a1.ready(), False)
        self.assertEqual(a1.successful(), False)
        a1.start()

        # states after start
        self.assertEqual(a1.started, True)
        self.assertEqual(a1.ready(), False)
        self.assertEqual(a1.successful(), False)

        a1.join()
        self.assertEqual(a1.started, False)
        self.assertEqual(a1.ready(), True)
        self.assertEqual(a1.successful(), True)
        
        self.assertEqual(a1.value, None)
        self.assertEqual(a1.exception, None)
        
        
