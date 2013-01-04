import sys
if '' not in sys.path:
    sys.path.append('')

import unittest

from pyactors.inbox import Postbox
from pyactors.inbox import DequeInbox
from pyactors.inbox import EmptyInboxException

class DequeInboxTest(unittest.TestCase):
    
    def test_deque_inbox(self):
        ''' test deque inbox
        '''
        inbox = DequeInbox()
        inbox.put({'command': 'start',})
        self.assertEqual(len(inbox), 1)
        self.assertEqual(inbox.get(), {'command': 'start',})
        self.assertEqual(len(inbox), 0)

    def test_deque_empty_inbox(self):
        ''' test deque inbox
        '''
        inbox = DequeInbox()
        self.assertRaises(EmptyInboxException, inbox.get)

class PostboxTest(unittest.TestCase):

    def test_postbox_send_msg(self):
        ''' send message via postbox
        '''
        inboxes = {
            'urn:uuid:001': DequeInbox(),
            'urn:uuid:002': DequeInbox(),
            'urn:uuid:003': DequeInbox(),
        }
        
        postbox = Postbox(inboxes)
        postbox.send('urn:uuid:001', 'msg-001')
        postbox.send('urn:uuid:002', 'msg-002')
        self.assertEqual(inboxes['urn:uuid:001'].get(), 'msg-001')
        self.assertEqual(inboxes['urn:uuid:002'].get(), 'msg-002')
        self.assertRaises(EmptyInboxException, inboxes['urn:uuid:002'].get, )

    def test_postbox_send_msg2(self):
        ''' send message via postbox
        '''
        inboxes = {
            'urn:uuid:001': DequeInbox(),
        }
        
        postbox = Postbox(inboxes)
        postbox.send('urn:uuid:001', 'msg-001')
        self.assertEqual(inboxes['urn:uuid:001'].get(), 'msg-001')

        inboxes['urn:uuid:002'] = DequeInbox()

        postbox.send('urn:uuid:002', 'msg-002')
        self.assertEqual(inboxes['urn:uuid:002'].get(), 'msg-002')

        inboxes['urn:uuid:003'] = DequeInbox()

        postbox.send('urn:uuid:003', 'msg-003')
        self.assertEqual(inboxes['urn:uuid:003'].get(), 'msg-003')

        self.assertRaises(EmptyInboxException, inboxes['urn:uuid:001'].get, )
        self.assertRaises(EmptyInboxException, inboxes['urn:uuid:002'].get, )
        self.assertRaises(EmptyInboxException, inboxes['urn:uuid:003'].get, )

        
