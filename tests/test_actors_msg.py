import sys
if '' not in sys.path:
    sys.path.append('')

import gevent
import logging
import unittest
import pyactors

_logger = logging.getLogger('test_actors_msg')

class ActorMsgTest(unittest.TestCase):
    
    def test_actor_send_msg(self):
        ''' test actor, send messages between actors
        '''
        class ActorA(pyactors.Actor):
            def _run(self):
                for actor in pyactors.find(actor_class_name='ActorB'):
                    self.postbox.send(actor.urn, 'message from ActorA')
                
        class ActorB(pyactors.Actor):
            def _run(self):
                while self.started:
                    msg = self.inbox.get()
                    if msg <> 'message from ActorA':
                        raise RuntimeError('No message from ActorA')
                    else:
                        self.value = msg
            
        pyactors.add(ActorA())
        pyactors.add(ActorB())
        gevent.sleep(0)
        for actor in pyactors.find(actor_class_name='ActorB'):
            self.assertEqual(actor.value, 'message from ActorA')

