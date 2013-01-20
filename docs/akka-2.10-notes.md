# Notes from Akka documentation, Release 2.10, Typesafe Inc.

Akka is Open Source and available under the Apache 2 License.
Download from http://typesafe.com/stack/downloads/akka/

Akka provides scalable real-time transaction processing. Akka is an unified runtime and programming model for:

- Scale up (Concurrency)
- Scale out (Remoting)
- Fault tolerance

Akka is very modular and consists of several JARs containing different features.

- akka-actor – Classic Actors, Typed Actors, IO Actor etc.
- akka-remote – Remote Actors
- akka-testkit – Toolkit for testing Actor systems
- akka-kernel – Akka microkernel for running a bare-bones mini application server
- akka-transactor – Transactors - transactional actors, integrated with Scala STM
- akka-agent – Agents, integrated with Scala STM
- akka-camel – Apache Camel integration
- akka-zeromq – ZeroMQ integration
- akka-slf4j – SLF4J Event Handler Listener
- akka-filebased-mailbox – Akka durable mailbox (find more among community projects)

## Actor Systems

Actors are objects which encapsulate state and behavior, they communicate exclusively by exchanging messages which are placed into the recipient’s mailbox. An actor system manages the resources it is configured to use in order to run the actors which it contains.

Actors naturally form hierarchies. One actor, which is to oversee a certain function in the program might want to split up its task into smaller, more manageable pieces. The quintessential feature of actor systems is that tasks are split up and delegated until they become small enough to be handled in one piece. If one actor does not have the means for dealing with a certain situation, it sends a
corresponding failure message to its supervisor, asking for help. The recursive structure then allows to handle failure at the right level.

The difficulty in designing such a system is how to decide who should supervise what. There is of course no single best solution, but there are a few guidelines which might be helpful:

- If one actor manages the work another actor is doing, e.g. by passing on sub-tasks, then the manager should supervise the child. The reason is that the manager knows which kind of failures are expected and how to handle them.
- If one actor carries very important data (i.e. its state shall not be lost if avoidable), this actor should source out any possibly dangerous sub-tasks to children it supervises and handle failures of these children as appropriate. Depending on the nature of the requests, it may be best to create a new child for each request, which simplifies state management for collecting the replies. This is known as the “Error Kernel Pattern” from Erlang.
- If one actor depends on another actor for carrying out its duty, it should watch that other actor’s liveness and act upon receiving a termination notice. This is different from supervision, as the watching party has no influence on the supervisor strategy, and it should be noted that a functional dependency alone is not a criterion for deciding where to place a certain child actor in the hierarchy.

Actors give you:

- Simple and high-level abstractions for concurrency and parallelism.
- Asynchronous, non-blocking and highly performant event-driven programming model.
- Very lightweight event-driven processes (approximately 2.7 million actors per GB RAM).

Actors can be:

- Classic Actors
- Typed Actors
- IO Actors
- Remote Actors

**Fault Tolerance**

- Supervisor hierarchies with “let-it-crash” semantics.
- Supervisor hierarchies can span over multiple JVMs to provide truly fault-tolerant systems.
- Excellent for writing highly fault-tolerant systems that self-heal and never stop.

**Location Transparency**

Everything in Akka is designed to work in a distributed environment: all interactions of actors use pure message
passing and everything is asynchronous.

**Transactors**

Transactors combine actors and Software Transactional Memory (STM) into transactional actors. It allows you to
compose atomic message flows with automatic retry and rollback.

## What is an Actor?

An actor is a container for State, Behavior, a Mailbox, Children and a Supervisor Strategy. All of this is encapsulated behind an Actor Reference.

**Actor Reference**

An actor object needs to be shielded from the outside in order to benefit from the actor model. Therefore, actors are represented to the outside using actor references, which are objects that can be passed around freely and without restriction. This split into inner and outer object enables transparency for all the desired operations: restarting an actor without needing to update references elsewhere, placing the actual actor object on remote hosts, sending messages to actors in completely different applications. But the most important aspect is that it is not possible to look inside an actor and get hold of its state from the outside, unless the actor unwisely publishes this information itself.


**State**

Actor objects will typically contain some variables which reflect possible states the actor may be in. This can be an explicit state machine (e.g. using the FSM module), or it could be a counter, set of listeners, pending requests, etc. These data are what make an actor valuable, and they must be protected from corruption by other actors. 

Because the internal state is vital to an actor’s operations, having inconsistent state is fatal. Thus, when the actor
fails and is restarted by its supervisor, the state will be created from scratch, like upon first creating the actor. This
is to enable the ability of self-healing of the system.

**Behavior**

Every time a message is processed, it is matched against the current behavior of the actor. Behavior means a function which defines the actions to be taken in reaction to the message at that point in time, say forward a request if the client is authorized, deny it otherwise. This behavior may change over time, e.g. because different clients obtain authorization over time, or because the actor may go into an “out-of-service” mode and later come back. These changes are achieved by either encoding them in state variables which are read from the behavior logic, or the function itself may be swapped out at runtime, see the become and unbecome operations. However, the initial behavior defined during construction of the actor object is special in the sense that a restart of the actor will reset its behavior to this initial one.

**Mailbox**

An actor’s purpose is the processing of messages, and these messages were sent to the actor from other actors (or from outside the actor system). The piece which connects sender and receiver is the actor’s mailbox: each actor has exactly one mailbox to which all senders enqueue their messages. Enqueuing happens in the time-order of send operations, which means that messages sent from different actors may not have a defined order at runtime due to the apparent randomness of distributing actors across threads. Sending multiple messages to the same target from the same actor, on the other hand, will enqueue them in the same order.

There are different mailbox implementations to choose from, the default being a FIFO: the order of the messages processed by the actor matches the order in which they were enqueued. This is usually a good default, but applications may need to prioritize some messages over others. In this case, a priority mailbox will enqueue not always at the end but at a position as given by the message priority, which might even be at the front. While using such a queue, the order of messages processed will naturally be defined by the queue’s algorithm and in general not be FIFO.

An important feature in which Akka differs from some other actor model implementations is that the current behavior must always handle the next dequeued message, there is no scanning the mailbox for the next matching one. Failure to handle a message will typically be treated as a failure, unless this behavior is overridden.

**Children**

Each actor is potentially a supervisor: if it creates children for delegating sub-tasks, it will automatically supervise them. The list of children is maintained within the actor’s context and the actor has access to it. Modifications to the list are done by creating (context.actorOf(...)) or stopping (context.stop(child)) children and these actions are reflected immediately. The actual creation and termination actions happen behind the scenes in an asynchronous way, so they do not “block” their supervisor.

**Supervisor Strategy**

The final piece of an actor is its strategy for handling faults of its children. Fault handling is then done transparently by Akka, applying one of the strategies described in Supervision and Monitoring for each incoming failure. As this strategy is fundamental to how an actor system is structured, it cannot be changed once an actor has been created.

Considering that there is only one such strategy for each actor, this means that if different strategies apply to the various children of an actor, the children should be grouped beneath intermediate supervisors with matching strategies, preferring once more the structuring of actor systems according to the splitting of tasks into sub-tasks.

**When an Actor Terminates**

Once an actor terminates, i.e. fails in a way which is not handled by a restart, stops itself or is stopped by its supervisor, it will free up its resources, draining all remaining messages from its mailbox into the system’s “dead letter mailbox” which will forward them to the EventStream as DeadLetters. The mailbox is then replaced within the actor reference with a system mailbox, redirecting all new messages to the EventStream as DeadLetters. This is done on a best effort basis, though, so do not rely on it in order to construct “guaranteed delivery”.

The reason for not just silently dumping the messages was inspired by our tests: we register the TestEventListener on the event bus to which the dead letters are forwarded, and that will log a warning for every dead letter received—this has been very helpful for deciphering test failures more quickly. It is conceivable that this feature may also be of use for other purposes.

## Actor Best Practices

1. Actors should be like nice co-workers: do their job efficiently without bothering everyone else needlessly and avoid hogging resources. Translated to programming this means to process events and generate responses (or more requests) in an event-driven manner. Actors should not block (i.e. passively wait while occupying a Thread) on some external entity—which might be a lock, a network socket, etc.—unless it is
unavoidable; in the latter case see below.

2. Do not pass mutable objects between actors. In order to ensure that, prefer immutable messages. If the encapsulation of actors is broken by exposing their mutable state to the outside, you are back in normal Java concurrency land with all the drawbacks.

3. Actors are made to be containers for behavior and state, embracing this means to not routinely send behavior within messages (which may be tempting using Scala closures). One of the risks is to accidentally share mutable state between actors, and this violation of the actor model unfortunately breaks all the properties which make programming in actors such a nice experience.

4. Top-level actors are the innermost part of your Error Kernel, so create them sparingly and prefer truly hierarchical systems. This has benefits wrt. fault-handling (both considering the granularity of configuration and the performance) and it also reduces the strain on the guardian actor, which is a single point of contention if over-used.

## Blocking Needs Careful Management

In some cases it is unavoidable to do blocking operations, i.e. to put a thread to sleep for an indeterminate time, waiting for an external event to occur. Examples are legacy RDBMS drivers or messaging APIs, and the underlying reason in typically that (network) I/O occurs under the covers. When facing this, you may be tempted to just wrap the blocking call inside a Future and work with that instead, but this strategy is too simple: you are quite likely to find bottle-necks or run out of memory or threads when the application runs under increased load.

The non-exhaustive list of adequate solutions to the “blocking problem” includes the following suggestions:

- Do the blocking call within an actor (or a set of actors managed by a router), making sure to configure a thread pool which is either dedicated for this purpose or sufficiently sized.
- Do the blocking call within a Future, ensuring an upper bound on the number of such calls at any point in time (submitting an unbounded number of tasks of this nature will exhaust your memory or thread limits).
- Do the blocking call within a Future, providing a thread pool with an upper limit on the number of threads which is appropriate for the hardware on which the application runs.
- Dedicate a single thread to manage a set of blocking resources (e.g. a NIO selector driving multiple channels) and dispatch events as they occur as actor messages.

The first possibility is especially well-suited for resources which are single-threaded in nature, like database handles which traditionally can only execute one outstanding query at a time and use internal synchronization to ensure this. A common pattern is to create a router for N actors, each of which wraps a single DB connection and handles queries as sent to the router. The number N must then be tuned for maximum throughput, which will vary depending on which DBMS is deployed on what hardware.


