# Introduction

## The actor model

An actor has the following characteristics:

 * It does not share state with anybody else.
 * It can have its own state.
 * It can only communicate with other actors by sending and receiving messages.
 * It can only send messages to actors whose address it has.
 * When an actor receives a message it may take actions like:
    - altering its own state, e.g. so that it can react differently to a future message,
    - sending messages to other actors, or
    - starting new actors.
 * None of the actions are required, and they may be applied in any order.
 * It only processes one message at a time. In other words, a single actor does not give you any concurrency, and it does not need to use e.g. locks to protect its own state.

## Greenlets

Greenlets, sometimes referred to as "green threads," are a lightweight structure that allows you to do some cooperative multithreading in Python without the system overhead of real threads (like the thread or threading module would use). The main thing to keep in mind when dealing with greenlets is that a greenlet will never yield to another greenlet unless it calls some function in gevent that yields. 

Note in particular how the greenlet didn't do anything until we called sleep(). sleep() is one of the functions in gevent which will yield to other greenlets. If you want to yield to other greenlets but don't care to wait a second if there's no one ready to run, you can call gevent.sleep(0).

(c) Just a little python, http://blog.pythonisito.com/2012/07/gevent-and-greenlets.html

### It does not share state with anybody else.

```python
class SimpleActor(Actor):
    pass
```

### It can have its own state.

### It can only communicate with other actors by sending and receiving messages.

### It can only send messages to actors whose address it has.

### When an actor receives a message it may take actions like:

- altering its own state, e.g. so that it can react differently to a future message,
- sending messages to other actors, or
- starting new actors.

### None of the actions are required, and they may be applied in any order.

### It only processes one message at a time. In other words, a single actor does not give you any concurrency, and it does not need to use e.g. locks to protect its own state.



## Links

## Useful info

**gevent** is a Python networking library that uses greenlet to provide a synchronous API on top of libevent event loop.

Features include:

- Fast event loop based on libevent (epoll on Linux, kqueue on FreeBSD).
- Lightweight execution units based on greenlet.
- API that re-uses concepts from the Python standard library (e.g. Event, Queue).
- Cooperative socket and ssl modules.
- Ability to use standard library and 3rd party modules written for standard blocking sockets (gevent.monkey).
- DNS queries performed through libevent-dns.
- Fast WSGI server based on libevent-http.

Home page, http://www.gevent.org/

**greenlet** A `greenlet` is a small independent pseudo-thread. Think about it as a small stack of frames; the outermost (bottom) frame is the initial function you called, and the innermost frame is the one in which the greenlet is currently paused. You work with greenlets by creating a number of such stacks and jumping execution between them. Jumps are never implicit: a greenlet must choose to jump to another greenlet, which will cause the former to suspend and the latter to resume where it was suspended. Jumping between greenlets is called `switching`.

Home page, http://greenlet.readthedocs.org/en/latest/

