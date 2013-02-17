import sys
if '' not in sys.path:
    sys.path.append('')

import logging

from pyactors.greenlet import GreenletActor
from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInboxException

def file_logger(name, filename):
    ''' returns file logger
    '''
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(filename)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    return logger
    
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

