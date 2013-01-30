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

    def test_actors_add_remove_child(self):
        
        parent = pyactors.Actor()
        parent.add_child(pyactors.Actor())
        parent.add_child(pyactors.Actor())
        parent.add_child(pyactors.Actor())
        self.assertEqual(len(parent.children), 3)
        
        for actor in parent.children:
            parent.remove_child(actor.address)
        self.assertEqual(len(parent.children), 0)

    def test_actors_find_child_by_address(self):
        
        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(address=child.address)), 1)
        parent.remove_child(child.address)
        
    def test_actors_find_child_by_address_list(self):
        
        parent = pyactors.Actor()
        children = [pyactors.Actor() for _ in range(10)]
        addresses = list()
        for actor in children:
            addresses.append(actor.address)
            parent.add_child(actor)
        self.assertEqual(len(parent.find(address=addresses)), 10)
        for actor in children:
            parent.remove_child(actor.address)    
            
    def test_actors_find_child_by_actor_class(self):
        
        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(actor_class=pyactors.Actor)), 1)
        parent.remove_child(child.address)

    def test_actors_find_child_by_actor_class_name(self):
        
        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(actor_class_name='Actor')), 1)
        parent.remove_child(child.address)
            
    def test_actors_find_child_by_actor_class_names(self):

        class TestActor(pyactors.Actor):
            pass
        
        parent = pyactors.Actor()
        children = [TestActor() for _ in range(10)]
        for actor in children:
            parent.add_child(actor)
        self.assertEqual(len(parent.find(actor_class_name='TestActor')), 10)
        for actor in children:
            parent.remove_child(actor.address)    
            
            
