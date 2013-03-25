from pyactors.actor import Actor 
from pyactors.generator import GeneratorActor
from pyactors.greenlets import GreenletActor

from tests.echoclient import request_response

from gevent.queue import Queue as gQueue

''' 
-------------------------------------------
Basic Actors
-------------------------------------------
'''
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
Greenlets
-------------------------------------------
'''
class TestGreenletActor(GreenletActor):
    ''' TestGreenletActor
    '''
    def __init__(self, name=None, logger=None):
        super(TestGreenletActor, self).__init__(name=name, logger=logger)
        self.empty_msg_counter = 0
    
    @staticmethod
    def imap_job(message):
        return 'imap_job:%s' % message

    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to imap_queue: %s' % (self.name, message))
        self.imap_queue.put(message)
        self.logger.debug('%s.on_receive(), messages in imap_queue: %d' % (self.name, len(self.imap_queue)))
        
    def on_handle(self):
        ''' on_handle
        '''
        self.logger.debug('%s.on_handle()' % (self.name,))
        message = self.imap.next()
            
        if message:
            if self.parent is not None:
                self.logger.debug('%s.on_handle(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_handle(), send "%s" to itself' % (self.name, message))
                self.send(message)
        else:
            self.empty_msg_counter += 1
        
        if self.empty_msg_counter > 10:
            self.stop()
                    
class EchoClientGreenletActor(GreenletActor):
    ''' EchoClientGreenletActor
    '''
    @staticmethod
    def imap_job(message):
        return request_response(message[0], message[1], 'imap_job:%s\n' % message[2])
    
    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to imap queue: %s' % (self.name, message))
        self.imap_queue.put(message)

    def on_handle(self):
        ''' on_handle
        '''
        self.logger.debug('%s.on_handle()' % (self.name,))
        message = self.imap.next()
        if message:
            message = message.strip()
            if self.parent is not None:
                self.logger.debug('%s.on_handle(), send "%s" to parent' % (self.name, message))
                self.parent.send(message)
            else:
                self.logger.debug('%s.on_handle(), send "%s" to itself' % (self.name, message))
                self.send(message)

        if len(self.inbox) == 0 and len(self.imap_queue) == 0 and self.imap.greenlets_count == 0:            
            self.stop()

class SenderGreenletActor(GreenletActor):
    ''' SenderGreenletActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverGreenletActor(GreenletActor):
    ''' ReceiverGreenletActor
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

            
