import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
import unittest

class ActorsEnvironmentTest(unittest.TestCase):
    ''' Actors Environment
    '''

    def test_env_register_unregister_actors(self):
        
        for _ in range(5):
            pyactors.register(pyactors.SimpleActor())
        self.assertEqual(len(pyactors.get_all()), 5)
        for actor in pyactors.get_all():
            pyactors.unregister(actor=actor)        
        self.assertEqual(len(pyactors.get_all()), 0)

    def test_env_get_by_unknown_urn(self):
        
        self.assertRaises(pyactors.IncorrectURNException, pyactors.get_by_urn, None)
        self.assertEqual(pyactors.get_by_urn(''), None)
        self.assertEqual(pyactors.get_by_urn(u''), None)

    def test_env_send_msg_actors(self):
        
        for _ in range(5):
            pyactors.register(pyactors.SimpleActor())
    
        a1 = pyactors.get_all()[1]
        a4 = pyactors.get_all()[4]
        a1.send(a4.urn, 'test message')
        self.assertEqual(a4.inbox.get(),'test message')

        for actor in pyactors.get_all():
            pyactors.unregister(actor=actor)        

    def test_env_run(self):
        
        for _ in range(5):
            pyactors.register(pyactors.SimpleActor())

        pyactors.run()        

        for actor in pyactors.get_all():
            pyactors.unregister(actor)

    def test_env_inherited_actors(self):
        
        class ActorA(pyactors.Actor):
            pass

        class ActorB(ActorA):
            pass

        ab = ActorB()
        pyactors.register(ab)
        pyactors.unregister(actor=ab)

    def test_env_register_none(self):
        
        self.assertRaises(RuntimeError, pyactors.register, None)
    
    def test_env_get_by_class(self):
        
        for _ in range(5):
            pyactors.register(pyactors.SimpleActor())

        self.assertEqual(len(pyactors.get_by_class(pyactors.SimpleActor)), 5)

        for actor in pyactors.get_all():
            pyactors.unregister(actor=actor)

    def test_env_get_by_class_name(self):
        
        for _ in range(5):
            pyactors.register(pyactors.SimpleActor())

        self.assertEqual(len(pyactors.get_by_class_name('SimpleActor')), 5)

        for actor in pyactors.get_all():
            pyactors.unregister(actor=actor)

    def test_env_broadcast(self):
        
        for _ in range(5):
            pyactors.register(pyactors.SimpleActor())

        # send test message to all actors
        pyactors.broadcast('test message')
        for actor in pyactors.get_all():
            self.assertEqual(actor.inbox.get(), 'test message')

        # send test message to all SimpleActors by class
        pyactors.broadcast('test message', pyactors.SimpleActor)
        for actor in pyactors.get_by_class(pyactors.SimpleActor):
            self.assertEqual(actor.inbox.get(), 'test message')

        # send test message to all SimpleActors by class name
        pyactors.broadcast('test message', 'SimpleActor')
        for actor in pyactors.get_by_class_name('SimpleActor'):
            self.assertEqual(actor.inbox.get(), 'test message')
        

        for actor in pyactors.get_all():
            pyactors.unregister(actor=actor)
        
