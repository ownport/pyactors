from pyactors.actor import Actor 
from pyactors.generator import GeneratorActor
''' 
-------------------------------------------
Basic Actors
-------------------------------------------
'''
class SimpleActor(Actor):

    def on_send(self):
        self.send('message')

    def on_receive(self, message):
        self.logger.debug('SimpleActor.on_receive()')
        if message:
            self.send('%s-response' % message)
        self.stop()

''' 
-------------------------------------------
Generators
-------------------------------------------
'''
class TestGeneratorActor(GeneratorActor):
    ''' TestGeneratorActor
    '''
    def __init__(self, name=None, logger=None, iters=10):
        super(TestGeneratorActor, self).__init__(name=name, logger=logger)
        self.iters = ['%s:%d' % (self.name, i) for i in range(iters)]
        self.logger.debug('%s.__init__(), iters: %s' % (self.name, self.iters))

    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), messages in inbox: %s' % (self.name, len(self.inbox)))
        self.send(message)
        self.logger.debug('%s.on_receive(), message: "%s" sent to itself' % (self.name, message))

    def on_send(self):
        try:        
            msg = self.iters.pop()
            self.logger.debug('%s.on_send(), message: "%s", iters: %s' % (self.name, msg, self.iters))
        except IndexError:
            self.logger.debug('%s.stop()' % self.name)
            self.stop()
            return
            
        if self.parent is not None:
            self.parent.send(msg)
            self.logger.debug('%s.on_send(), message "%s" sent to parent' % (self.name, msg))
        else:
            self.send(msg)
            self.logger.debug('%s.on_send(), message "%s" sent to itself' % (self.name, msg))
        self.logger.debug('%s.on_send(), messages in inbox: %s' % (self.name, len(self.inbox)))

class ParentActor(GeneratorActor):
    ''' Parent Actor
    '''
    def on_send(self):
        self.logger.debug('%s.on_send(), children: %s' % (self.name, self.children))    

class SenderGeneratorActor(GeneratorActor):
    ''' SenderGeneratorActor
    '''
    def on_send(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_send(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_send(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverGeneratorActor(GeneratorActor):
    ''' ReceiverGeneratorActor
    '''
    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.parent.send(message)
            else:
                self.send(message)
            self.stop()

