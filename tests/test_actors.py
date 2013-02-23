import sys
if '' not in sys.path:
    sys.path.append('')

import unittest
import pyactors

from pyactors.logs import file_logger

class ActorTest(unittest.TestCase):

    def test_create(self):
        ''' test_actors.test_create
        '''
        test_name = 'test_actors.test_create'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = pyactors.Actor()
        self.assertFalse(actor.processing)
        self.assertIsNotNone(actor)

    def test_address(self):
        ''' test_actors.test_address
        '''
        test_name = 'test_actors.test_address'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = pyactors.Actor()
        self.assertNotEqual(actor.address, None)
        self.assertTrue(type(actor.address) == str)
        self.assertEqual(len(actor.address), 32)

    def test_properties(self):
        ''' test_actors.test_properties
        '''
        test_name = 'test_actors.test_properties'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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

    def test_run_not_implemented(self):
        ''' test_run_not_implemented
        '''
        test_name = 'test_actors.test_run_not_implemented'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = pyactors.Actor()
        self.assertRaises(RuntimeError, actor.run)
        self.assertRaises(RuntimeError, actor.run_once)

    def test_loop_not_implemented(self):
        ''' test_loop_not_implemented
        '''
        test_name = 'test_actors.test_loop_not_implemented'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = pyactors.Actor()
        self.assertRaises(RuntimeError, actor.loop)

    def test_add_remove_child(self):
        ''' test_actors.test_add_remove_child
        '''
        test_name = 'test_actors.test_add_remove_child'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = pyactors.Actor()
        parent.add_child(pyactors.Actor())
        parent.add_child(pyactors.Actor())
        parent.add_child(pyactors.Actor())
        self.assertEqual(len(parent.children), 3)
        
        for actor in parent.children:
            parent.remove_child(actor.address)
        self.assertEqual(len(parent.children), 0)

    def test_add_existing_actor(self):
        ''' test_add_existing_actor
        '''
        test_name = 'test_actors.test_add_existing_actor'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertRaises(RuntimeError, parent.add_child, child)

    def test_remove_non_existing_actor(self):
        ''' test_remove_non_existing_actor
        '''
        test_name = 'test_actors.test_remove_non_existing_actor'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = pyactors.Actor()
        child = pyactors.Actor()
        self.assertRaises(RuntimeError, parent.remove_child, child.address)

    def test_find_children(self):
        ''' test_actors.test_find_children
        '''
        test_name = 'test_actors.test_find_children'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find()), 1)
        parent.remove_child(child.address)

    def test_find_child_by_address(self):
        ''' test_actors.test_find_child_by_address
        '''
        test_name = 'test_actors.test_find_child_by_address'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(address=child.address)), 1)
        parent.remove_child(child.address)
        
    def test_find_child_by_address_list(self):
        ''' test_actors.test_find_child_by_address_list
        '''
        test_name = 'test_actors.test_find_child_by_address_list'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = pyactors.Actor()
        children = [pyactors.Actor() for _ in range(10)]
        addresses = list()
        for actor in children:
            addresses.append(actor.address)
            parent.add_child(actor)
        self.assertEqual(len(parent.find(address=addresses)), 10)
        for actor in children:
            parent.remove_child(actor.address)    
            
    def test_find_child_by_actor_class(self):
        ''' test_actors.test_find_child_by_actor_class
        '''
        test_name = 'test_actors.test_find_child_by_actor_class'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = pyactors.Actor()
        child = pyactors.Actor()
        parent.add_child(child)
        self.assertEqual(len(parent.find(actor_class=pyactors.Actor)), 1)
        parent.remove_child(child.address)

    def test_find_child_by_actor_name(self):
        ''' test_actors.test_find_child_by_actor_name
        '''
        test_name = 'test_actors.test_find_child_by_actor_name'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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

            
    def test_find_child_by_actor_names(self):
        ''' test_actors.test_find_child_by_actor_names
        '''
        class TestActor(pyactors.Actor):
            pass
        
        test_name = 'test_actors.test_child_by_actor_names'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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

    def test_find_childs_of_grandparents(self):
        ''' test_actors.test_find_childs_of_grandparents
        '''
        test_name = 'test_actors.test_find_childs_of_grandparents'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

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
        
