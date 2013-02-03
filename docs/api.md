# pyactors API

## class Actor

### def __init__(self, name=None)

Actor's constructor. If `name` is not defined class name will be used.

### def __str__(self)

represent actor as string

### def waiting(self)

Property. Return True if actor is waiting for new messages

### def processing(self)

Property. Return True if actor is processing 

### def add_child(self, actor)

add actor's child

### def remove_child(self, address)

remove child by its address


### def children(self):
Property. Return list of actor's children


### def find(self, address=None, actor_class=None, actor_name=None):

find children by criterias 
        
- if no criterias are defined, return all children addresses
    
- if `address` is defined as string or unicode, return an actor by its address.
- if `address` is defined as list or tuple, return actors by thier addresses.
        
- if `actor_class` is defined as string or unicode, return the list of all existing actors of the given class, or of any subclass of the given class.
- if `actor_class` is defined as list or tuple, return actors by thier actor classes.
        
- if `actor_name` is defined, return the list of all existing actors of the given name.
        
### def start(self):

start actor

### def stop(self):

stop actor

### def run(self):

run actor
        
### def run_once(self):

run actor for one iteraction

### def send(self, message):

send message to actor

### def loop(self):

processing loop, used for actor without children

### def supervise(self):

supervising loop, used when actor has children

