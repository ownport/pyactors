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


