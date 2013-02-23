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

At the moment pyactors supported only 4 approaches for working with actors: generators, greenlets, threads and processes. Based on this 5 actors can be created:

- GeneratorActor, based on generators
- GreenletActor, based on gevent library & greenlets
- ThreadedGeneratorActor, the same as GeneratorActor but the actor created in separated thread
- ForkedGeneratorActor, the same as GeneratorActor but the actor created in separated process
- ForkedGreenletActor, the same as GreenletActor but the actor created in separated process

GeneratorActor is basic actor. There's no need to install external library, standard python library is enough. The principle is the same as for greenlet but based on python generators. Switchover between actors performed by `yield` inside `loop()` method. The example of GeneratorActor:
```
class TestActor(GeneratorActor):
    def loop(self):
        for i in range(10):
            if self.processing:
                self.parent.send(i)
            else:
                break
            yield
        self.stop()
```
The same actor but based on greenlet will be:
```
class TestActor(GreenletActor):
    def loop(self):
        for i in range(10):
            if self.processing:
                self.parent.send(i)
            else:
                break
            self.sleep()
        self.stop()
```
As you can see from the code above the difference between GeneratorActor and GreenletActor is in switching method between actors. In GeneratorActor case it's `yield`. In GreenletActor it's `self.sleep()`.

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
More examples how to use actors with pyactors can be founded in [unittests](https://github.com/ownport/pyactors/tree/master/tests)

## Actor's children matrix

 | Generator | Greenlet | ThreadedGenerator | ForkedGenerator | ForkedGreenlet
--- | --- | --- | --- | --- | ---
Generator | X | X | X | X | X
Greenlet | | X | | | X
ThreadedGenerator | X | X | | |
ForkedGenerator | X | X | X | |
ForkedGreenlet | | X | | |


