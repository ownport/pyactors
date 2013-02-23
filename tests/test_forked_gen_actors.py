import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest

from pyactors.logs import file_logger
#from pyactors.generator import GeneratorActor
#from pyactors.forked import ForkedGeneratorActor
from pyactors.exceptions import EmptyInboxException

from tests import ForkedGenActor
from tests import TestGeneratorActor as TestActor
from tests import SenderGeneratorActor as SenderActor
from tests import ReceiverGeneratorActor as ReceiverActor
from tests import ForkedLongRunningActor as LongRunningActor

class ForkedGeneratorActorTest(unittest.TestCase):

    def test_run(self):
        ''' test_forked_gen_actors.test_run
        '''
        test_name = 'test_forked_gen_actors.test_run'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = ForkedGenActor()
        logger.debug('ForkedGenActor-%d' % id(actor))
        actor.start()
        while actor.processing:
            time.sleep(0.5)
        actor.stop()
        logger.debug('ForkedGenActor-%d.stopped' % id(actor))

        result = []
        while True:
            try:
                result.append(actor.inbox.get())
            except EmptyInboxException:
                break

        self.assertEqual(len(result), 10)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_stop_in_the_middle(self):
        ''' test_forked_gen_actors.test_stop_in_the_middle
        '''  
        test_name = 'test_forked_gen_actors.test_stop_in_the_middle'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        actor = LongRunningActor()
        logger.debug('LongRunningActor-%d' % id(actor))
        actor.start()
        self.assertEqual(actor.processing, True)
        logger.debug('timeout started')
        time.sleep(0.5)
        logger.debug('timeout stopped')
        logger.debug('actor stop')
        actor.stop()
        logger.debug('actor stopped')

        result = []
        while True:
            try:
                result.append(actor.inbox.get())
            except EmptyInboxException:
                break
        self.assertGreater(result, 0)

        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)
        #assert False, 'test_actors_stop_in_the_middle'

    def test_processing_with_children(self):
        ''' test_forked_gen_actors.test_processing_with_children
        '''    
        test_name = 'test_forked_gen_actors.test_processing_with_children'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = ForkedGenActor()      
        for _ in range(5):
            parent.add_child(TestActor())      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 50)

        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        
    def test_processing_with_diff_timelife_children(self):
        ''' test_forked_gen_actors.test_processing_with_diff_timelife_children
        '''    
        test_name = 'test_forked_gen_actors.test_processing_with_diff_timelife_children'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = ForkedGenActor()      
        for i in range(5):
            parent.add_child(TestActor(iters=i))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(result, [0,0,0,0,1,1,1,3,3,6])
        self.assertEqual(len(result), 10)

        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)
        

    def test_send_msg_between_actors(self):
        ''' test_forked_gen_actors.test_send_msg_between_actors
        '''        
        test_name = 'test_forked_gen_actors.test_send_msg_between_actors'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = ForkedGenActor()      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual(parent.inbox.get(), 'message from sender') 

    def test_forked_actor_in_actor(self):
        ''' test_forked_gen_actors.test_actors_actor_in_actor
        '''
        test_name = 'test_forked_gen_actors.test_forked_actor_in_actor'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        parent = ForkedGenActor(name='Parent')              
        logger.debug('%s' % parent)
        
        parent.add_child(ForkedGenActor(name='Child-1'))
        parent.add_child(ForkedGenActor(name='Child-2'))      
        logger.debug('%s, children: %s' % (parent, [str(child) for child in parent.children]))

        parent.start()
        logger.debug('%s, actor started' % parent)

        while parent.processing:
            logger.debug('%s, actor is processing' % parent)
            time.sleep(0.1)
        parent.stop()       
        logger.debug('%s, actor stopped' % parent)

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 20)

        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)

    def test_send_msg_between_forked_actors(self):
        ''' test_forked_gen_actors.test_send_msg_between_forked_actors
        '''        
        test_name = 'test_forked_gen_actors.test_send_msg_between_forked_actors'
        logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

        # TODO
        '''
        parent = ForkedGenActor(name='ForkedSenderReceiver')      
        parent.add_child(ForkedSenderActor(name='ForkedSender'))      
        parent.add_child(ForkedReceiverActor(name='ForkedReceiver'))      
        parent.start()
        time_start = time.time()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        '''

if __name__ == '__main__':
    unittest.main()
    
