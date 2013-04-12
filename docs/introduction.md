# Introduction

Simple implementation actors on python. Experimental project. It's attempt to merge generators, greenlets, threads and processes under actor concept.

## Installation

The pyactors's sources are available on [github](https://github.com/ownport/pyactors) or it's available as the library via pip:
```
$ pip install pyactors
```

## Building blocks

The basic class for creation actors is Actor class. It defines the collection of common methods and properties for all actors: name, start(), stop(), parent, add_child(), children, remove_child(), run(), run_once(), join(), send(), find(). See [PyActors API](https://github.com/ownport/pyactors/blob/master/docs/api.md) for more details.

The actor is independent processing unit. The actor has three essential elements of computation. It has in body: processing, storage, communication. The communication between actors is based on sending or receiving messages. Two methods are used for these purposes: on_receive() and on_handle().

- on_receive() method is called in case when actor received message

```python
class SimpleActor(pyactors.actor.Actor):
    def on_receive(self, message):
        self.storage.put(message)
```

- on_handle() method is called every time when actor gets control. It can be used when actor should send message even incoming message is not received. As example: actor is used as generator for message series.

```python
class SimpleActor(pyactors.actor.Actor):
    def on_handle(self):
        try:
            self.send('message')
        except StopReceived:
            pass
```

The actor can create new actors as a child by `add_child()` method or remove it by `remove_child()`. The actor with children performs supervising role for its children. The supervising logic handled in _supervise_loop().

- start()

- joinall()

## Actor types

At the moment pyactors supported 3 approaches for working with actors: generators, greenlets and threads. Based on this 3 actors can be created:

- GeneratorActor, based on generators
- GreenletActor, based on GeneratorActor and imap_nonblocking function
- ThreadedGeneratorActor, the same as GeneratorActor but the actor created in separated thread

GeneratorActor is basic actor. There's no need to install external library, standard python library is enough. The example, GeneratorActor:
```python
class Receiver(GeneratorActor):
    ''' Receiver
    '''
    def on_receive(self, message):
        self.logger.debug('%s.on_receive(), message: %s' % (self.name, message))
        if message:
            self.logger.debug('%s.on_receive(), send "%s" to itself' % (self.name, message))
            self.send(message)
            self.stop()
```
The actor above waiting for a message, as soon as a message received the actor sends this messages to itself. Another example:
```python
class Sender(GeneratorActor):
    ''' Sender
    '''
    def on_handle(self):
        receivers = [r for r in self.find(actor_name='Receiver')]
        self.logger.debug('%s.on_handle(), receivers: %s' % (self.name, receivers))
        for actor in receivers:
            actor.send('message from sender')
            self.logger.debug('%s.on_handle(), message sent to actor %s' % (self.name, actor))
        self.stop()
```
In this example the actor sends message to all active actors who has a name `Receiver` and then stops it work. If it's needed you can combine both these methods in one actor.

If you need to work with network environment better to use gevent library. This library allows you to avoid blocking network operations. For this purpose pyactors contains GreenletActor class. It's the same actor as GeneratorActor but extended with imap_nonblocking function for running many greenlets under one actor. To get more information about greenlets, please visit [gevent](http://www.gevent.org/) home page. Direct access to imap_nonblocking function is hidden but you can define a method which will be spawned in imap_nonblocking function. GreenletActor has predefined name for this method: 
```python
class SimpleActor(GreenletActor):
    ''' To be defined soon
    '''
    pass
```
As you can see from the code above the difference between GeneratorActor and GreenletActor is predefined method `imap` which contains greenlet code. GreenletActor class was added as template for using gevent library. You need to have another behaviour for working with gevent, you can create your own class based on GeneratorActor.

**Note** Before using GreenletActor please check that gevent is installed
```
$ pip install gevent
```
The ThreadedGeneratorActor, ForkedGeneratorActor, ForkedGreenletActor are the same as GeneratorActor and GreenletActor but in first case the actor will be created in separate thread, in second and third cases in separate processes.

To run actor 
```
actor = TestActor()
actor.start()
actor.run()
actor.stop()
```
More examples how to use actors with pyactors can be founded in [tests](https://github.com/ownport/pyactors/tree/master/tests)

## Actor's parent/children matrix

Recommended combination of Actor's parents and children. 

Parent/Children | Generator | Greenlet | ThreadedGenerator 
--- | --- | --- | --- 
Generator | X | X | X 
Greenlet | X | X | X 
ThreadedGenerator | X | X | 

## System messages

The [system messages](https://github.com/ownport/pyactors/blob/master/docs/system-msg.md) are used in pyactors for actor's management and monitoring. 


