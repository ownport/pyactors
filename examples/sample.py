#!/usr/bin/env python
#   
#   sample
#     
import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.actors import actor_status

class SampleActor(pyactors.actors.Actor):

    def loop(self):
        for i in range(10):
            for actor in pyactors.get_by_class_name('PrintActor'):
                self.postbox.send(actor.urn, 'message-%d' % i)
            yield actor_status.processing
        yield actor_status.waiting

class PrintActor(pyactors.actors.Actor):
        
    def loop(self):
        while True:
            try:
                message = self.inbox.get()
            except pyactors.inbox.EmptyInboxException:
                yield actor_status.waiting
                continue
            print self.__class__.__name__, self.urn, message    
            yield actor_status.processing

p_actor_urn = pyactors.register(PrintActor())
s_actor_urn = pyactors.register(SampleActor())

pyactors.run()

for actor in pyactors.get_all():
    pyactors.unregister(actor=actor)

