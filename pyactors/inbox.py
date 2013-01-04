
__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__license__ = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

import collections

class EmptyInboxException(Exception):
    ''' Exception raised when Inbox is empty
    '''
    pass

''' Classes
'''

class Postbox(object):
    ''' postbox for sending messages to actors
    '''
    def __init__(self, inboxes):
        ''' init postbox
        
        inboxes - the dictionary for active actors 
        '''
        self.__inboxes = inboxes

    def send(self, urn, message):
        ''' send message to actor by URN
        '''
        if urn not in self.__inboxes:
            raise ActorDeadException(urn)
        
        self.__inboxes[urn].put(message)

class DequeInbox(object):
    ''' Inbox from collections.deque
    '''
    def __init__(self):
        ''' __init__ 
        '''
        super(DequeInbox, self).__init__()
        self.__inbox = collections.deque()
                    
    def get(self):
        ''' get data from inbox 
        '''
        try:
            result = self.__inbox.popleft()
        except IndexError:
            raise EmptyInboxException
        return result
    
    def put(self, message):
        ''' put message to inbox 
        '''
        self.__inbox.append(message)
    
    def __len__(self):
        ''' return length of inbox
        '''
        return len(self.__inbox)


