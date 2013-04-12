''' 
-------------------------------------------
Basic Actors
-------------------------------------------
'''
from pyactors.actor import Actor 
from pyactors.inbox import DequeInbox

class StorageActor(Actor):
    ''' Simple actor with storage
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(StorageActor, self).__init__(name=name, logger=logger)
        self.storage = DequeInbox()

class SimpleActor(StorageActor):

    def on_handle(self):
        try:
            self.send('message')
        except:
            self.stop()

    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self._name, message))
        self.storage.put('%s-response' % message)
        self.stop()

''' 
-------------------------------------------
Generators
-------------------------------------------
'''
from pyactors.generator import GeneratorActor

class StorageGeneratorActor(GeneratorActor):
    ''' Simple actor with storage
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(StorageGeneratorActor, self).__init__(name=name, logger=logger)
        self.storage = DequeInbox()

class ParentGeneratorActor(StorageGeneratorActor):
    ''' Parent Actor
    '''
    def on_handle(self):
        self.logger.debug('%s.on_handle(), children: %s' % (self.name, self.children))    
        if len(self.children) == 0:
            self.stop()

    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), messages in inbox: %s' % (self.name, len(self.inbox)))
        self.logger.debug('%s.on_receive(), message: "%s" sent to storage' % (self.name, message))
        self.storage.put(message)

class TestGeneratorActor(StorageGeneratorActor):
    ''' TestGeneratorActor
    '''
    def __init__(self, name=None, logger=None, iters=10):
        super(TestGeneratorActor, self).__init__(name=name, logger=logger)
        self.iters = ['%s:%d' % (self.name, i) for i in range(iters)]
        self.logger.debug('%s.__init__(), messages in queue: %s' % (self.name, self.iters))

    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), messages in queue: %s' % (self.name, len(self.inbox)))
        self.logger.debug('%s.on_receive(), message: "%s" sent to storage' % (self.name, message))
        self.storage.put(message)

    def on_handle(self):
        try:        
            msg = self.iters.pop()
            self.logger.debug('%s.on_handle(), messages in queue: %s' % (self.name, self.iters))
        except IndexError:
            self.logger.debug('%s.stop()' % self.name)
            self.stop()
            return
            
        if self.parent is not None:
            self.logger.debug('%s.on_handle(), message "%s" sent to parent' % (self.name, msg))
            try:
                self.parent.send(msg)
            except:
                self.logger.debug('%s.on_handle(), parent stopped: %s' % (self.name, self.parent))
        else:
            self.logger.debug('%s.on_handle(), message "%s" sent to storage' % (self.name, msg))
            self.storage.put(msg)
            
        self.logger.debug('%s.on_handle(), messages in child inbox: %s' % (self.name, len(self.inbox)))

class SenderGeneratorActor(StorageGeneratorActor):
    ''' SenderGeneratorActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverGeneratorActor(StorageGeneratorActor):
    ''' ReceiverGeneratorActor
    '''
    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_receive(), send "%s" to storage' % (self.name, message))
                self.storage.put(message)
            self.stop()

''' 
-------------------------------------------
ThreadedActors
-------------------------------------------
'''
from pyactors.thread import ThreadedGeneratorActor

class StorageThreadedGeneratorActor(ThreadedGeneratorActor):
    ''' Simple actor with storage
    '''
    def __init__(self, name=None, logger=None):
        ''' __init__
        '''
        super(StorageThreadedGeneratorActor, self).__init__(name=name, logger=logger)
        self.storage = DequeInbox()

class TestThreadedGeneratorActor(StorageThreadedGeneratorActor):
    ''' TestThreadedGeneratorActor
    '''
    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to imap_queue: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                try:
                    self.parent.send(message)
                except:
                    self.logger.debug('%s.on_receive(), parent stopped: %s' % (self.name, self.parent))
            else:
                self.logger.debug('%s.on_receive(), send "%s" to storage' % (self.name, message))
                self.storage.put(message)
        
    def on_handle(self):
        ''' on_handle
        '''
        self.logger.debug('%s.on_handle()' % (self.name,))
        if len(self.inbox) == 0:
            self.stop()

class SenderThreadedActor(StorageThreadedGeneratorActor):
    ''' SenderThreadedActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            try:
                actor.send('message from sender')
            except:
                self.logger.debug('%s.on_handle(), receiver-actor stopped: %s' % (self.name, actor))
            
        self.stop()

class ReceiverThreadedActor(StorageThreadedGeneratorActor):
    ''' ReceiverGeneratorActor
    '''
    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self.name, message))
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_receive(), send "%s" to parent' % (self.name, message))
                try:
                    self.parent.send(message)
                except:
                    self.logger.debug('%s.on_receive(), parent stopped: %s' % (self.name, self.parent))
                
            else:
                self.logger.debug('%s.on_receive(), send "%s" to storage' % (self.name, message))
                self.storage.put(message)
                
            self.stop()

            
                        
