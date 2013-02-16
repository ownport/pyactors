import sys
if '' not in sys.path:
    sys.path.append('')

import logging
logger = logging.getLogger(__name__)

import unittest
import pyactors


class ActorTest(unittest.TestCase):

    def test_actors_create(self):
        ''' test_actors.test_actors_create
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_create' % __name__)
        actor = pyactors.Actor()
        self.assertFalse(actor.processing)
        self.assertIsNotNone(actor)

    def test_actors_address(self):
        ''' test_actors.test_actors_address
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_address' % __name__)
        actor = pyactors.Actor()
        self.assertNotEqual(actor.address, None)
        self.assertTrue(type(actor.address) == str)
        self.assertEqual(len(actor.address), 32)

    def test_actors_properties(self):
        ''' test_actors.test_actors_properties
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_properties' % __name__)
        actor = pyactors.Actor(name='test_actor')
        self.assertTrue(isinstance(str(actor), str))
        self.assertEqual(actor.name, 'test_actor')

        try:
            actor.family
        except RuntimeError:
            pass

        try:
            actor.waiting = 1
        except RuntimeError:
            pass

        try:
            actor.processing = 1
        except RuntimeError:
            pass

    def test_actors_run_not_implemented(self):
        ''' test_actors_run_not_implemented
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_run_not_implemented' % __name__)
        actor = pyactors.Actor()
        self.assertRaises(RuntimeError, actor.run)

    def test_actors_loop_not_implemented(self):
        ''' test_actors_loop_not_implemented
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_loop_not_implemented' % __name__)
        actor = pyactors.Actor()
        self.assertRaises(RuntimeError, actor.loop)

    def test_actors_add_remove_child(self):
        ''' test_actors.test_actors_add_remove_child
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_add_remove_child' % __name__)
        parent = pyactors.Actor()
        parent.add_child(pyactors.Actor())
        parent.add_child(pyactors.Actor())
        parent.add_child(pyactors.Actor())
        self.assertEqual(len(parent.children), 3)
        
        for actor in parent.children:
            parent.remove_child(actor.address)
        self.assertEqual(len(parent.children), 0)

    def test_actors_find_child_by_address(self):
        ''' test_actors.test_actors_find_child_by_address
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_find_child_by_address' % __name__)
        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(address=child.address)), 1)
        parent.remove_child(child.address)
        
    def test_actors_find_child_by_address_list(self):
        ''' test_actors.test_actors_find_child_by_address_list
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_find_child_by_address_list' % __name__)
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
        ''' test_actors.test_actors_find_child_by_actor_class
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_find_child_by_actor_class' % __name__)
        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(actor_class=pyactors.Actor)), 1)
        parent.remove_child(child.address)

    def test_actors_find_child_by_actor_name(self):
        ''' test_actors.test_actors_find_child_by_actor_name
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_find_child_by_actor_name' % __name__)
        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(actor_name='Actor')), 1)
        parent.remove_child(child.address)

        # name is defined        
        parent = pyactors.Actor(name='Parent')
        child = pyactors.Actor(name='Child')
        parent.add_child(child)
        self.assertEqual(len(parent.find(actor_name='Child')), 1)
        parent.remove_child(child.address)

            
    def test_actors_find_child_by_actor_names(self):
        ''' test_actors.test_actors_find_child_by_actor_names
        '''
        class TestActor(pyactors.Actor):
            pass
        
        logger = logging.getLogger('%s.ActorTest.test_actors_find_child_by_actor_names' % __name__)
        parent = pyactors.Actor()
        children = [TestActor() for _ in range(10)]
        for actor in children:
            parent.add_child(actor)
        self.assertEqual(len(parent.find(actor_name='TestActor')), 10)
        for actor in children:
            parent.remove_child(actor.address)    
            
        # name is defined        
        parent = pyactors.Actor(name='Parent')
        children = [TestActor(name='Child-TestActor') for _ in range(10)]
        for actor in children:
            parent.add_child(actor)
        self.assertEqual(len(parent.find(actor_name='Child-TestActor')), 10)
        for actor in children:
            parent.remove_child(actor.address)    

    def test_actors_find_childs_of_grandparents(self):
        ''' test_actors.test_actors_find_childs_of_grandparents
        '''
        logger = logging.getLogger('%s.ActorTest.test_actors_find_childs_of_grandparents' % __name__)
        grandparent = pyactors.Actor(name='grandparent')
        for _ in range(3):
            grandparent.add_child(pyactors.Actor(name='parent'))
        for parent in grandparent.children:
            for _ in range(2):
                parent.add_child(pyactors.Actor(name='child'))            
        self.assertEqual(len(grandparent.children[0].children[0].find(actor_name='grandparent')), 1)
        self.assertEqual(len(grandparent.children[0].children[0].find(actor_name='parent')), 3)
        self.assertEqual(len(grandparent.children[0].children[0].find(actor_name='child')), 2)
        
        
if __name__ == '__main__':
    unittest.main()
        
