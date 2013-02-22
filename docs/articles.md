# Articles

## Actor model

An actor has the following characteristics:

- It does not share state with anybody else.
- It can have its own state.
- It can only communicate with other actors by sending and receiving messages.
- It can only send messages to actors whose address it has.
- When an actor receives a message it may take actions like:
    - altering its own state, e.g. so that it can react differently to a future message,
    - sending messages to other actors, or
    - starting new actors.
- None of the actions are required, and they may be applied in any order.
- It only processes one message at a time. In other words, a single actor does not give you any concurrency, and it does not need to use e.g. locks to protect its own state.

### Links

- [Actor Model (Wikipedia)](http://en.wikipedia.org/wiki/Actor_model)
- [Actor model theory (Wikipedia)](http://en.wikipedia.org/wiki/Actor_model_theory)

## Akka

- [Notes from Akka documentation, Release 2.10, Typesafe Inc.](https://github.com/ownport/pyactors/blob/master/docs/articles.md)

## Gevent

[gevent](http://www.gevent.org/) is a Python networking library that uses greenlet to provide a synchronous API on top of libevent event loop.

Features include:

- Fast event loop based on libevent (epoll on Linux, kqueue on FreeBSD).
- Lightweight execution units based on greenlet.
- API that re-uses concepts from the Python standard library (e.g. Event, Queue).
- Cooperative socket and ssl modules.
- Ability to use standard library and 3rd party modules written for standard blocking sockets (gevent.monkey).
- DNS queries performed through libevent-dns.
- Fast WSGI server based on libevent-http.

### Articles

- [gevent: the Good, the Bad, the Ugly](http://code.mixpanel.com/2010/10/29/gevent-the-good-the-bad-the-ugly/) 
- [Gevent and Greenlets](http://blog.pythonisito.com/2012/07/gevent-and-greenlets.html) 
- [Introduction to Gevent](http://blog.pythonisito.com/2012/07/introduction-to-gevent.html) 
- [Gevent, Threads, and Benchmarks](http://blog.pythonisito.com/2012/07/gevent-threads-and-benchmarks.html) 
- [gevent. For the Working Python Developer](http://sdiehl.github.com/gevent-tutorial/)

## greenlet

A [greenlet](http://greenlet.readthedocs.org/en/latest/) is a small independent pseudo-thread. Think about it as a small stack of frames; the outermost (bottom) frame is the initial function you called, and the innermost frame is the one in which the greenlet is currently paused. You work with greenlets by creating a number of such stacks and jumping execution between them. Jumps are never implicit: a greenlet must choose to jump to another greenlet, which will cause the former to suspend and the latter to resume where it was suspended. Jumping between greenlets is called `switching`.s

Greenlets, sometimes referred to as "green threads," are a lightweight structure that allows you to do some cooperative multithreading in Python without the system overhead of real threads (like the thread or threading module would use). The main thing to keep in mind when dealing with greenlets is that a greenlet will never yield to another greenlet unless it calls some function in gevent that yields. 

Note in particular how the greenlet didn't do anything until we called sleep(). sleep() is one of the functions in gevent which will yield to other greenlets. If you want to yield to other greenlets but don't care to wait a second if there's no one ready to run, you can call gevent.sleep(0).

(c) Just a little python, http://blog.pythonisito.com/2012/07/gevent-and-greenlets.html

## eventlet

[eventlet](http://eventlet.net/doc/index.html) is built around the concept of green threads (i.e. coroutines, we use the terms interchangeably) that are launched to do network-related work. Green threads differ from normal threads in two main ways:

- Green threads are so cheap they are nearly free. You do not have to conserve green threads like you would normal threads. In general, there will be at least one green thread per network connection.
- Green threads cooperatively yield to each other instead of preemptively being scheduled. The major advantage from this behavior is that shared data structures don’t need locks, because only if a yield is explicitly called can another green thread have access to the data structure. It is also possible to inspect primitives such as queues to see if they have any pending data.

## Another actor's projects on python

- [Message Passing Conccurrency (Actor Model) in Python](http://www.valuedlessons.com/2008/06/message-passing-conccurrency-actor.html)
- [Pykka](http://pykka.readthedocs.org/en/latest/) is easy to use concurrency for Python using the actor model

## Python conccurrency

The presentation ["An introduction to Python concurrency"](http://www.slideshare.net/dabeaz/an-introduction-to-python-concurrency)




