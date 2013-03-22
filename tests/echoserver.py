#!/usr/bin/env python
#
#   simple server
#   used for testing greenlet actors
#

__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
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

import settings
from packages import pyservice

# -----------------------------------------------
# handlers
# -----------------------------------------------

def handle(socket, address):
    socket.send("simple server: %s\n" % dir(socket))
    socket.close()

# -----------------------------------------------
# SimpleServerService
# -----------------------------------------------
class SimpleServerService(pyservice.Process):
    ''' SimpleServerService
    '''
    pidfile = settings.SIMPLE_SERVER_PIDFILE
    logfile = settings.SIMPLE_SERVER_LOGFILE

    def run(self):
        ''' run
        '''
        from gevent.server import StreamServer
        
        self.logger.info('SimpleServerService.run() started')
        params = (settings.SIMPLE_SERVER_IP_ADDRESS, settings.SIMPLE_SERVER_IP_PORT)
        StreamServer(params, handle).serve_forever()
    
# -----------------------------------------------
# main
# -----------------------------------------------
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2 and sys.argv[1] in 'start stop restart status'.split():
        pyservice.service('simple_server.SimpleServerService', sys.argv[1])
    else:
        print 'usage: simple_server.py <start,stop,restart,status>'
    
