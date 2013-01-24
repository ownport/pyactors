import sys
if '' not in sys.path:
    sys.path.append('')

import logging
import unittest
import pyactors

from gevent.queue import Queue
from pyactors.messages import Postbox

_logger = logging.getLogger('test_postbox')

class PostboxTest(unittest.TestCase):
    
    def test_postbox_create(self):
        ''' test postbox, create
        '''
        postbox = Postbox()
        self.assertTrue(postbox is not None)
        self.assertTrue(isinstance(postbox, Postbox))        
        
    def test_postbox_add_inbox(self):
        ''' test postbox, add inbox
        '''
        queue = Queue()
        postbox = Postbox()
        postbox.add('urn:uuid:0001', queue)
        
    def test_postbox_remove_inbox(self):
        ''' test postbox, add/remove inbox
        '''
        queue = Queue()
        postbox = Postbox()
        
        postbox.add('urn:uuid:0001', queue)
        postbox.remove('urn:uuid:0001')

    def test_postbox_send_msg(self):
        ''' test postbox, send message
        '''
        queue = Queue()
        postbox = Postbox()
        postbox.add('urn:uuid:0001', queue)
        
        postbox.send('urn:uuid:0001', 'test message #1')
        postbox.send('urn:uuid:0001', 'test message #2')
        postbox.send('urn:uuid:0001', 'test message #3')
        self.assertEqual(queue.qsize(), 3)
        self.assertEqual(queue.get(), 'test message #1')
        self.assertEqual(queue.get(), 'test message #2')
        self.assertEqual(queue.get(), 'test message #3')
        self.assertTrue(queue.empty())
        
        postbox.remove('urn:uuid:0001')
        
