# Introduction

Simple implementation actors on python. Experimental project. It's attempt to merge generators, greenlets, threads and processes under actor concept.

## Installation

The pyactors's sources are available on [github](https://github.com/ownport/pyactors) or as the library via pip:
```
$ pip install pyactors
```

## Building blocks

The basic class for creation actors is Actor class. It defines the collection of common methods and properties for all actors: name, processing, waiting, start(), stop(), parent, add_child(), children, remove_child(), run(), loop(), supervise(), send(), find(). See [PyActors API](https://github.com/ownport/pyactors/blob/master/docs/api.md) for more details.

All logics for processing data in the actor is located in `loop()` method. There's no embedded mechanism for switching between actors, developers should care about it by themsleves.

The actor can create new actors as a child by `add_child()` method or remove it by `remove_child()`. The actor without children is processing actor and `loop()` method is used for handling data. An actor becomes a superviser if the actor has children. Only `supervise()` method is used for managing children-actors.

## Actor types

At the moment pyactors supported 4 approaches for working with actors: generators, greenlets, threads and processes. Based on this 5 actors can be created:

- GeneratorActor, based on generators
- GreenletActor, based on GeneratorActor and imap_nonblocking function
- ThreadedGeneratorActor, the same as GeneratorActor but the actor created in separated thread
- ForkedGeneratorActor, the same as GeneratorActor but the actor created in separated process
- ForkedGreenletActor, the same as GreenletActor but the actor created in separated process

GeneratorActor is basic actor. There's no need to install external library, standard python library is enough. The principle is the same as for greenlet but based on python generators. Switchover between actors performed by `yield` inside `loop()` method. The example of GeneratorActor:
```python
class TestActor(GeneratorActor):
    ''' To be defined soon
    '''
    pass
```
If you need to work with network environment better to use gevent library. For this purpose pyactors contains GreenletActor class. It's the same actor as GeneratorActor but extended with imap_nonblocking function. This function allows you to run many greenlets under one actor.
```python
class TestActor(GreenletActor):
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

Parent/Children | Generator | Greenlet | ThreadedGenerator | ForkedGenerator | ForkedGreenlet
--- | --- | --- | --- | --- | ---
Generator | X | X | X | X | X
Greenlet | X | X | X | X | X
ThreadedGenerator | X | X | | |
ForkedGenerator | X | X | X | |
ForkedGreenlet | X | X | | |

## System messages

The [system messages](https://github.com/ownport/pyactors/blob/master/docs/system-msg.md) are used in pyactors for actor's management and monitoring. 


