# System message

The system messages are used in pyactors for actor's management and monitoring. The system message is python dictionary with the next structure:

```
'system-msg': 
    'type': stop | echo-request | echo-response, 
    'sender': <actor-address>,
```

## Command 'stop'

The parent actor can send `stop` message to the child actor. As soon as the child actor receives this message from parent, it's run `stop` method

```
'system-msg': 
    'type': stop,
    'sender': <parent-actor-address>,
```

## Command 'echo-request' and 'echo-response'

Time to time the parent can ask children about their status: is it alive?. It can be done by sending `echo-request` and `echo-response` messages.

```
'system-msg': 
    'type': echo-request,
    'sender': <actor-address (parent)>,
```

As response to request

```
'system-msg': 
    'type': echo-response,
    'sender': <actor-address (child)>,
```


