import sys
if '' not in sys.path:
    sys.path.append('')

import logging
import unittest
import pyactors

_logger = logging.getLogger('test_actor_system')

class ActorTest(unittest.TestCase):
    
    def test_actor_system(self):
        ''' test actor system 
        '''
        # check that actor system is not None
        self.assertTrue(pyactors._actor_system <> None)
        # check that actor system is ActorSystem()
        self.assertTrue(isinstance(pyactors._actor_system, pyactors.ActorSystem))

    def test_actor_system_add_actor(self):
        ''' test actor system, add actor
        '''
        actor = pyactors.Actor()
        # trying to add something
        self.assertRaises(RuntimeError, pyactors.add, None)
        # actor added to the system successfuly
        self.assertTrue(pyactors.add(actor).startswith('urn:uuid:'))
        # check second attempt to add existing actor
        self.assertRaises(RuntimeError, pyactors.add, actor)
        pyactors.remove(actor.urn)

    def test_actor_system_add_inherited_actor(self):
        ''' test actor system, add inherited actor
        '''
        
        class SimpleActor(pyactors.Actor):
            pass
        # add SimpleActor inherited from Actor class
        simple_actor = SimpleActor()
        self.assertTrue(pyactors.add(simple_actor).startswith('urn:uuid:'))
        pyactors.remove(simple_actor.urn)

    def test_actor_system_remove_actor(self):
        ''' test actor system, remove actor
        '''
        # add / remove actor by actor urn
        actor = pyactors.Actor()
        pyactors.add(actor)
        pyactors.remove(actor.urn)

    def test_actor_system_find_all(self):
        ''' test actor system, find all existing actors in the system
        '''
        # get list of all actors in the system
        actor_urns = list()
        for i in range(10):
            actor_urns.append(pyactors.add(pyactors.Actor()))
        
        self.assertGreaterEqual(len(set(pyactors.find()) - set(actor_urns)), 0) 

        for urn in actor_urns:
            pyactors.remove(urn)

        self.assertGreaterEqual(len(pyactors.find()), 0) 

    def test_actor_system_find_by_one_urn(self):
        ''' test actor system, find actor in the system by one urn
        '''
        # get actor by urn
        actor = pyactors.Actor()
        pyactors.add(actor)
        self.assertEqual(pyactors.find(urn=actor.urn), [actor,]) 
        pyactors.remove(actor.urn)
    
    def test_actor_system_find_by_many_urns(self):
        ''' test actor system, find actor in the system by many urns
        '''

        # get actor by many urns
        actor_urns = list()
        for i in range(10):
            actor_urns.append(pyactors.add(pyactors.Actor()))

        selected_urns = actor_urns[2:5]
        self.assertEqual(len(pyactors.find(urn=selected_urns)), 3) 

        for urn in actor_urns:
            pyactors.remove(urn)

    def test_actor_system_find_by_actor_class(self):
        ''' test actor system, find actor in the system by actor class
        '''
        class ActorA(pyactors.Actor):
            pass
        class ActorB(pyactors.Actor):
            pass
        class ActorC(pyactors.Actor):
            pass

        actors = [ActorA(), ActorB(), ActorB(), ActorC(), ActorC(), ActorC()]
        for actor in actors:
            pyactors.add(actor)

        self.assertEqual(len(pyactors.find(actor_class=ActorA)), 1)
        self.assertEqual(len(pyactors.find(actor_class=ActorB)), 2)
        self.assertEqual(len(pyactors.find(actor_class=ActorC)), 3)

        for actor in actors:
            pyactors.remove(actor.urn)

    def test_actor_system_find_by_actor_class_name(self):
        ''' test actor system, find actor in the system by actor class name
        '''
        class ActorA(pyactors.Actor):
            pass
        class ActorB(pyactors.Actor):
            pass
        class ActorC(pyactors.Actor):
            pass

        actors = [ActorA(), ActorB(), ActorB(), ActorC(), ActorC(), ActorC()]
        for actor in actors:
            pyactors.add(actor)

        self.assertEqual(len(pyactors.find(actor_class_name='ActorA')), 1)
        self.assertEqual(len(pyactors.find(actor_class_name='ActorB')), 2)
        self.assertEqual(len(pyactors.find(actor_class_name='ActorC')), 3)

        for actor in actors:
            pyactors.remove(actor.urn)

