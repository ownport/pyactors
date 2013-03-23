# For developers

## GreenletActors

For testing GreenletActors, pyactors library contains echo server (tests/echoserver.py) which can be runned as service in background.

```
$ tests/echoserver.py start
Starting process with EchoService...
$ tests/echoserver.py stop
Stopping process EchoService...
$ tests/echoserver.py status
Process is not running
``` 

To simplify working with echo server, you can use echoclient.py library. It can be runned as standalone console application for sending/receiving messages between echo server.
```
$ tests/echoclient.py "Test message"
Test message
$
```

