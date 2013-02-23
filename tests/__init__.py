import sys
if '' not in sys.path:
    sys.path.append('')

import logging

from pyactors.greenlet import GreenletActor
from pyactors.generator import GeneratorActor
from pyactors.forked import ForkedGeneratorActor
from pyactors.forked import ForkedGreenletActor
from pyactors.exceptions import EmptyInboxException
    
''' 
-------------------------------------------
Generators
-------------------------------------------
'''
class TestGeneratorActor(GeneratorActor):
    ''' TestGeneratorActor
    '''
    def __init__(self, name=None, iters=10):
        super(TestGeneratorActor, self).__init__(name=name)
        self.iters = iters
    
    def loop(self):
        ''' loop
        '''
        result = 0
        for i in range(self.iters):
            if self.processing:
                result += i
                if self.parent is not None:
                    self.parent.send(result)
                else:
                    self.send(result)
                yield
            else:
                break
        self.stop()

class SenderGeneratorActor(GeneratorActor):
    ''' SenderGeneratorActor
    '''
    def loop(self):
        for actor in self.find(actor_name='Receiver'):
            actor.send('message from sender')
        self.stop()

class ReceiverGeneratorActor(GeneratorActor):
    ''' ReceiverGeneratorActor
    '''
    def loop(self):
        while self.processing:
            try:
                message = self.inbox.get()    
            except EmptyInboxException:
                self._waiting = True
                yield
                
            if message:
                if self.parent is not None:
                    self.parent.send(message)
                else:
                    self.send(message)
                break
        self.stop()

''' 
-------------------------------------------
Greenlets
-------------------------------------------
'''
class TestGreenletActor(GreenletActor):
    ''' TestGreenletActor
    '''
    def __init__(self, name=None, iters=10):
        super(TestGreenletActor, self).__init__(name=name)
        self.iters = iters
    
    def loop(self):
        ''' loop
        '''
        result = 0
        for i in range(self.iters):
            if self.processing:
                result += i
                if self.parent is not None:
                    self.parent.send(result)
                else:
                    self.send(result)
            else:
                break
            self.sleep()
        self.stop()

class SenderGreenletActor(GreenletActor):
    ''' SenderGreenletActor
    '''
    def loop(self):
        receiver_founded = False
        while self.processing:
            for actor in self.find(actor_name='Receiver'):
                actor.send('message from sender')
                receiver_founded = True
            if receiver_founded:
                break
        self.stop()

class ReceiverGreenletActor(GreenletActor):
    ''' ReceiverGreenletActor
    '''
    def __init__(self, name=None):
        super(ReceiverGreenletActor, self).__init__(name=name)
        
    def loop(self):
        ''' loop
        '''
        message = None
        while self.processing:
            try:
                message = self.inbox.get()    
            except EmptyInboxException:
                self._waiting = True
                
            if message:
                if self.parent is not None:
                    self.parent.send(message)
                else:
                    self.send(message)
                break
            
            self.sleep()
        self.stop()

''' 
-------------------------------------------
Forked Actors
-------------------------------------------
'''
class ForkedGenActor(ForkedGeneratorActor):
    ''' Forked Generator Actor
    '''
    def loop(self):
        ''' loop
        '''
        result = 0
        for i in xrange(10):
            if self.processing:
                result += i
                if self.parent is not None:
                    self.parent.send(result)
                else:
                    self.send(result)
                yield
            else:
                break
        self.stop()

class ForkedLongRunningActor(ForkedGeneratorActor):
    ''' ForkedLongRunningActor
    '''
    def __init__(self, name=None, logger=None):
        super(ForkedLongRunningActor, self).__init__(name=name, logger=logger)
        self.result = 0

    def loop(self):
        while self.processing:
        #for i in range(100):
            if self.processing:
                self.result += 1
                if self.parent is not None:
                    self.parent.send(self.result)
                yield
            else:
                break
        self.stop()

class ForkedGreActor(ForkedGreenletActor):
    ''' Forked Greenlet Actor (test)
    '''
    def __init__(self, name=None, logger=None):
        super(ForkedGreActor, self).__init__(name=name, logger=logger)
        self.result = 0
    
    def loop(self):
        for i in xrange(10):
            if self.processing:
                self.result += i
                if self.parent is not None:
                    self.parent.send(self.result)
                else:
                    self.send(self.result)
                self.sleep()
            else:
                break
        self.stop()

