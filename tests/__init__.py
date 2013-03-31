''' 
-------------------------------------------
Basic Actors
-------------------------------------------
'''
from pyactors.actor import Actor 

class SimpleActor(Actor):

    def on_handle(self):
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
from pyactors.generator import GeneratorActor

class ParentGeneratorActor(GeneratorActor):
    ''' Parent Actor
    '''
    def on_handle(self):
        self.logger.debug('%s.on_handle(), children: %s' % (self.name, self.children))    
        if len(self.children) == 0:
            self.stop()

    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), messages in inbox: %s' % (self.name, len(self.inbox)))
        self.send(message)
        self.logger.debug('%s.on_receive(), message: "%s" sent to itself' % (self.name, message))
                    

class TestGeneratorActor(GeneratorActor):
    ''' TestGeneratorActor
    '''
    def __init__(self, name=None, logger=None, iters=10):
        super(TestGeneratorActor, self).__init__(name=name, logger=logger)
        self.iters = ['%s:%d' % (self.name, i) for i in range(iters)]
        self.logger.debug('%s.__init__(), messages in queue: %s' % (self.name, self.iters))

    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), messages in queue: %s' % (self.name, len(self.inbox)))
        self.send(message)
        self.logger.debug('%s.on_receive(), message: "%s" sent to itself' % (self.name, message))

    def on_handle(self):
        try:        
            msg = self.iters.pop()
            self.logger.debug('%s.on_handle(), messages in queue: %s' % (self.name, self.iters))
        except IndexError:
            self.logger.debug('%s.stop()' % self.name)
            self.stop()
            return
            
        if self.parent is not None:
            self.parent.send(msg)
            self.logger.debug('%s.on_handle(), message "%s" sent to parent' % (self.name, msg))
        else:
            self.send(msg)
            self.logger.debug('%s.on_handle(), message "%s" sent to itself' % (self.name, msg))
        self.logger.debug('%s.on_handle(), messages in child inbox: %s' % (self.name, len(self.inbox)))

class SenderGeneratorActor(GeneratorActor):
    ''' SenderGeneratorActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverGeneratorActor(GeneratorActor):
    ''' ReceiverGeneratorActor
    '''
    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_receive(), send "%s" to itself' % (self.name, message))
                self.send(message)
            self.stop()

''' 
-------------------------------------------
ThreadedActors
-------------------------------------------
'''
from pyactors.thread import ThreadedGeneratorActor

class TestThreadedGeneratorActor(ThreadedGeneratorActor):
    ''' TestThreadedGeneratorActor
    '''
    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to imap_queue: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_receive(), send "%s" to itself' % (self.name, message))
                self.send(message)
        
    def on_handle(self):
        ''' on_handle
        '''
        self.logger.debug('%s.on_handle()' % (self.name,))
        if len(self.inbox) == 0:
            self.stop()

class SenderThreadedActor(ThreadedGeneratorActor):
    ''' SenderThreadedActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverThreadedActor(ThreadedGeneratorActor):
    ''' ReceiverGeneratorActor
    '''
    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_receive(), send "%s" to itself' % (self.name, message))
                self.send(message)
            self.stop()

''' 
-------------------------------------------
ForkedActors
-------------------------------------------
'''
from pyactors.inbox import ProcessInbox

class ForkedParentActor(GeneratorActor):
    ''' Parent Actor
    '''
    def __init__(self, name, logger):
        ''' __init__
        '''
        super(ForkedParentActor, self).__init__(name=name, logger=logger)
        self.inbox = ProcessInbox()
    
    def on_handle(self):
        self.logger.debug('%s.on_handle(), children: %s' % (self.name, self.children))    
        if len(self.children) == 0:
            self.stop()

    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), messages in inbox: %s' % (self.name, len(self.inbox)))
        self.send(message)
        self.logger.debug('%s.on_receive(), message: "%s" sent to itself' % (self.name, message))

            
                        
