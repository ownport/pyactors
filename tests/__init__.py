import sys
if '' not in sys.path:
    sys.path.append('')

from pyactors.greenlet import GreenletActor
from pyactors.generator import GeneratorActor
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
        super(TestGeneratorActor, self).__init__()
        self.result = 0
        self.iters = iters
    
    def loop(self):
        for i in range(self.iters):
            if self.processing:
                self.result += i
                if self.parent is not None:
                    self.parent.send(self.result)
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
    def __init__(self, name=None):
        super(ReceiverGeneratorActor, self).__init__(name=name)
        
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
        self.result = 0
        self.iters = iters
    
    def loop(self):
        for i in range(self.iters):
            if self.processing:
                self.result += i
                if self.parent is not None:
                    self.parent.send(self.result)
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
        self.message = None
        
    def loop(self):
        while self.processing:
            try:
                self.message = self.inbox.get()    
            except EmptyInboxException:
                self._waiting = True
                
            if self.message:
                break
            
            self.sleep()
        self.stop()

