# For developers

## GreenletActors

For testing GreenletActors, pyactors library contains simple socket server (tests/simple_server.py) which can be runned as service in background.

```
$ tests/simple_server.py start
Starting process with SimpleServerService...
$ tests/simple_server.py stop
Stopping process SimpleServerService...
$ tests/simple_server.py status
Process is not running
``` 

