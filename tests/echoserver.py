#!/usr/bin/env python
#
#   echo server
#   used for testing greenlet actors
#
#   based on examples/echoserver.py 
#   from https://github.com/SiteSupport/gevent/blob/master/examples/echoserver.py
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

def echo(socket, address):
    ''' echo
    '''
    fileobj = socket.makefile()
    line = fileobj.readline()
    if not line:
        fileobj.close()
        return
    fileobj.write(line)
    fileobj.flush()
    fileobj.close()

# -----------------------------------------------
# EchoService
# -----------------------------------------------
class EchoService(pyservice.Process):
    ''' EchoService
    '''
    pidfile = settings.ECHO_SERVER_PIDFILE
    logfile = settings.ECHO_SERVER_LOGFILE

    def run(self):
        ''' run
        '''
        from gevent.server import StreamServer
        
        self.logger.info('EchoService.run() started')
        params = (settings.ECHO_SERVER_IP_ADDRESS, settings.ECHO_SERVER_IP_PORT)
        StreamServer(params, echo).serve_forever()
    
def usage():
    print 'usage: echoserver.py <start,stop,restart,status>'

    
# -----------------------------------------------
# main
# -----------------------------------------------
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2 and sys.argv[1] in 'start stop restart status'.split():
        pyservice.service('echoserver.EchoService', sys.argv[1])
    else:
        usage()
        
