# Notes from Akka documentation, Release 2.10, Typesafe Inc.

Akka is Open Source and available under the Apache 2 License.
Download from http://typesafe.com/stack/downloads/akka/

**Actors**

Actors give you:
- Simple and high-level abstractions for concurrency and parallelism.
- Asynchronous, non-blocking and highly performant event-driven programming model.
- Very lightweight event-driven processes (approximately 2.7 million actors per GB RAM).

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


