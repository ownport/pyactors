import sys
if '' not in sys.path:
    sys.path.append('')

import logging
import unittest
import pyactors

_logger = logging.getLogger('actors_test')

class ActorTest(unittest.TestCase):
    
    def test_actor_urn(self):
        ''' test actor URN
        '''
        a1 = pyactors.actors.Actor()
        self.assertTrue(a1.urn.startswith('urn:uuid:'))

    def test_actor_unsucc_send(self):
        ''' unsuccessful sending message to actor
        '''
        a1 = pyactors.actors.Actor()
        self.assertRaises(
                            pyactors.actors.NonRegisteredActorException, 
                            a1.send, 'urn:uuid:00000', 'test message'
        )
        
    def test_actor_run(self):
        
        from pyactors.actors import actor_status
        
        class SampleActor(pyactors.actors.Actor):

            def loop(self):
                for i in range(10):
                    for actor in pyactors.get_by_class_name('PrintActor'):
                        self.postbox.send(actor.urn, 'message-%d' % i)
                    yield actor_status.processing
                yield actor_status.waiting

        class PrintActor(pyactors.actors.Actor):
                
            def loop(self):
                while True:
                    try:
                        message = self.inbox.get()
                    except pyactors.inbox.EmptyInboxException:
                        yield actor_status.waiting
                        continue
                    print message    
                    yield actor_status.processing
        
        p_actor_urn = pyactors.register(PrintActor())
        s_actor_urn = pyactors.register(SampleActor())
        
        pyactors.run()
        
        for actor in pyactors.get_all():
            pyactors.unregister(actor=actor)

