import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.generator import GeneratorActor
from pyactors.exceptions import EmptyInboxException

''' 
-------------------------------------------
ForkedGeneratorActors
-------------------------------------------
'''
from pyactors.forked import ForkedGeneratorActor
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

class TestForkedGeneratorActor(ForkedGeneratorActor):
    ''' TestForkedGeneratorActor
    '''
    def on_receive(self, message):
        ''' on_receive
        '''
        self.logger.debug('%s.on_receive(), sent message to parent: %s' % (self.name, message))
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

class SenderForkedGeneratorActor(ForkedGeneratorActor):
    ''' SenderForkedGeneratorActor
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
            self.stop()

class ReceiverForkedGeneratorActor(ForkedGeneratorActor):
    ''' ReceiverForkedGeneratorActor
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
ForkedGreenletActors
-------------------------------------------
'''
from pyactors.forked import ForkedGreenletActor

class TestForkedGreenletActor(ForkedGreenletActor):
    ''' TestForkedGreenletActor
    '''
    pass
    


''' 
-------------------------------------------
Tests
-------------------------------------------
'''
def test_run():
    ''' test_forked_actors.test_run
    '''
    test_name = 'test_forked_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ForkedParentActor(name='Parent',logger=logger)
    child = TestForkedGeneratorActor(name='Child', logger=logger)
    parent.add_child(child)
    for i in range(10):
        child.send(test_name)
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    assert len(result) == 10, "len(result): %d, %s" % (len(result), result)
    assert result == [test_name for _ in range(10)], result

