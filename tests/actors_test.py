import sys
if '' not in sys.path:
    sys.path.append('')

import unittest
from pyactors.actors import Actor
from pyactors.actors import NonRegisteredActorException

class ActorTest(unittest.TestCase):
    
    def test_actor_urn(self):
        ''' test actor URN
        '''
        a1 = Actor()
        self.assertTrue(a1.urn.startswith('urn:uuid:'))

    def test_actor_unsucc_send(self):
        ''' unsuccessful sending message to actor
        '''
        a1 = Actor()
        self.assertRaises(NonRegisteredActorException, a1.send, 'urn:uuid:00000', 'test message')
        
        
