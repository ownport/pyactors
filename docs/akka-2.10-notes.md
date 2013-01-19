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

**Actors**

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


