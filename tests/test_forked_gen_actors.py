import sys
if '' not in sys.path:
    sys.path.append('')

import time
import unittest
import logging
_logger = logging.getLogger(__name__)

from pyactors.generator import GeneratorActor
from pyactors.forked import ForkedGeneratorActor
from pyactors.exceptions import EmptyInboxException

from tests import file_logger
from tests import TestGeneratorActor as TestActor
from tests import SenderGeneratorActor as SenderActor
from tests import ReceiverGeneratorActor as ReceiverActor

LOGFILE = 'logs/test_forked_gen_actors.log'        

class ForkedGenActor(ForkedGeneratorActor):
    ''' Forked Generator Actor
    '''
    def __init__(self, name=None):
        ''' __init__
        '''
        super(ForkedGenActor, self).__init__(name=name)
        self._logger = file_logger('%s.%s' % (__name__, str(self)), filename=LOGFILE) 
    
    def loop(self):
        ''' loop
        '''
        result = 0
        for i in xrange(10):
            if self.processing:
                self._logger.debug('i: %d' % (i))
                result += i
                if self.parent is not None:
                    self.parent.send(result)
                else:
                    self.send(result)
                yield
            else:
                break
        self._logger.debug('stop()')
        self.stop()
        self._logger.debug('processing: %s' % (self.processing))

class LongRunningActor(ForkedGeneratorActor):
    ''' LongRunningActor
    '''
    def __init__(self, name=None):
        super(LongRunningActor, self).__init__(name=name)
        self._logger = file_logger('%s.LongRunningActor' % __name__, filename='logs/test_forked_gen_actors.log') 
        self._logger.debug('LongRunningActor-%d' % id(self))
        self.result = 0

    def loop(self):
        while self.processing:
        #for i in range(100):
            if self.processing:
                self._logger.debug('id: %d, result: %d' % (id(self),self.result))
                self.result += 1
                if self.parent is not None:
                    self.parent.send(self.result)
                yield
            else:
                break
        self._logger.debug('LongRunningActor.stop()')
        self.stop()

class ForkedGeneratorActorTest(unittest.TestCase):

    def test_actors_run(self):
        ''' test_forked_gen_actors.test_actors_run
        '''
        print 'test_forked_gen_actors.test_actors_run'
        _logger = file_logger('%s.test_actors_run' % __name__, filename='logs/test_forked_actors_run.log') 
        actor = ForkedGenActor()
        _logger.debug('ForkedGenActor-%d' % id(actor))
        actor.start()
        while actor.processing:
            time.sleep(0.5)
        actor.stop()
        _logger.debug('ForkedGenActor-%d.stopped' % id(actor))

        result = []
        while True:
            try:
                result.append(actor.inbox.get())
            except EmptyInboxException:
                break

        self.assertEqual(len(result), 10)
        self.assertEqual(actor.processing, False)
        self.assertEqual(actor.waiting, False)

    def test_actors_stop_in_the_middle(self):
        ''' test_forked_gen_actors.test_actors_stop_in_the_middle
        '''  
        print 'test_forked_gen_actors.test_actors_stop_in_the_middle'
        _logger = file_logger('%s.test_actors_stop_in_the_middle' % __name__, filename='logs/test_forked_actors_stop_in_the_middle.log') 
        actor = LongRunningActor()
        _logger.debug('LongRunningActor-%d' % id(actor))
        actor.start()
        self.assertEqual(actor.processing, True)
        _logger.debug('timeout started')
        time.sleep(0.5)
        _logger.debug('timeout stopped')
        _logger.debug('actor stop')
        actor.stop()
        _logger.debug('actor stopped')

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

    def test_actors_processing_with_children(self):
        ''' test_forked_gen_actors.test_actors_processing_with_children
        '''    
        print 'test_forked_gen_actors.test_actors_processing_with_children'
        logger = logging.getLogger('%s.ForkedGeneratorActorTest.test_actors_processing_with_children' % __name__)
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
        
    def test_actors_processing_with_diff_timelife_children(self):
        ''' test_forked_gen_actors.test_actors_processing_with_diff_timelife_children
        '''    
        print 'test_forked_gen_actors.test_actors_processing_with_diff_timelife_children'
        logger = logging.getLogger('%s.ForkedGeneratorActorTest.test_actors_processing_with_diff_timelife_children' % __name__)
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
        

    def test_actors_send_msg_between_actors(self):
        ''' test_forked_gen_actors.test_actors_send_msg_between_actors
        '''        
        print 'test_forked_gen_actors.test_actors_send_msg_between_actors'
        logger = logging.getLogger('%s.ForkedGeneratorActorTest.test_actors_send_msg_between_actors' % __name__)
        parent = ForkedGenActor()      
        parent.add_child(SenderActor(name='Sender'))      
        parent.add_child(ReceiverActor(name='Receiver'))      
        parent.start()
        while parent.processing:
            time.sleep(0.1)
        parent.stop()       
        self.assertEqual(parent.inbox.get(), 'message from sender') 

    def test_actors_forked_actor_in_actor(self):
        ''' test_forked_gen_actors.test_actors_forked_actor_in_actor
        '''
        _logger = file_logger('%s.test_forked_actor_in_actor' % __name__, filename=LOGFILE) 
        
        parent = ForkedGenActor(name='Parent')              
        _logger.debug('%s' % parent)
        
        parent.add_child(ForkedGenActor(name='Child-1'))
        parent.add_child(ForkedGenActor(name='Child-2'))      
        _logger.debug('%s, children: %s' % (parent, [str(child) for child in parent.children]))

        parent.start()
        _logger.debug('%s, actor started' % parent)

        while parent.processing:
            _logger.debug('%s, actor is processing' % parent)
            time.sleep(0.1)
        parent.stop()       
        _logger.debug('%s, actor stopped' % parent)

        result = []
        while True:
            try:
                result.append(parent.inbox.get())
            except EmptyInboxException:
                break
        self.assertEqual(len(result), 20)

        self.assertEqual(parent.processing, False)
        self.assertEqual(parent.waiting, False)

    def test_actors_send_msg_between_forked_actors(self):
        ''' test_forked_gen_actors.test_actors_send_msg_between_forked_actors
        '''        
        print 'test_forked_gen_actors.test_actors_send_msg_between_forked_actors'
        logger = logging.getLogger('%s.ForkedGeneratorActorTest.test_actors_send_msg_between_forked_actors' % __name__)
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
    
