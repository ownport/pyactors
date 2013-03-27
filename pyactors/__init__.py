__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__version__ = '0.3.0-new-actor-flow' 
__license__ = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

import sys

PY3 = sys.version_info[0] >= 3

'''
Utilities
'''        

def joinall(actors):
    ''' wait until actors finished
    '''
    stopped_actors = list()
    if not isinstance(actors, (list, tuple)):
        raise RuntimeError('Actors shoud be list')
        
    while True:
        for actor in actors:
            if actor.address in stopped_actors:
                continue
            if not actor.run_once():
                stopped_actors.append(actor.address)
                    
        if len(actors) == len(stopped_actors):
            break
                

def killall(actors):
    ''' kill all actors in the list
    '''
    if not isinstance(actors, (list, tuple)):
        raise RuntimeError('Actors shoud be list')
        
    for actor in actors:
        actor.stop()
    
