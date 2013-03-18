#!/usr/bin/env python
#
#   HTTP server, based on bottle.py
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

import json
import logging
import settings

from packages import bottle
from packages.bottle import request

from packages import pyservice

# monkey patching for BaseHTTPRequestHandler.log_message
def log_message(obj, format, *args):
    logging.info("%s %s" % (obj.address_string(), format % args))

class BottlePyService(pyservice.Process):
    ''' BottlePyService
    '''
    pidfile = settings.HTTP_SERVER_PIDFILE
    logfile = settings.HTTP_SERVER_LOGFILE

    def __init__(self):
        ''' __init__
        '''
        super(BottlePyService, self).__init__()
        
        from BaseHTTPServer import BaseHTTPRequestHandler
        BaseHTTPRequestHandler.log_message = log_message

    def run(self):
        logging.info('http_server/bootle-{} server starting up'.format(bottle.__version__))
        bottle.run(host='localhost', port=8800, debug=settings.DEBUG_MODE)
    
# -----------------------------------------------
# handlers
# -----------------------------------------------

def get_request_dict():
    ''' get_request_dict
    '''
    d = {}
    d['url'] = request.url
    d['path'] = request.path
    d['fullpath'] = request.fullpath
    d['method'] = request.method
    d['remote_addr'] = request.remote_addr
    d['headers'] = dict(request.headers)
    return json.dumps(d)    

@bottle.route('/', method=['GET',])
def handle_get_index():
    ''' handle GET/index
    '''
    return get_request_dict()

# -----------------------------------------------
# main
# -----------------------------------------------
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2 and sys.argv[1] in 'start stop restart status'.split():
        pyservice.service('http_server.BottlePyService', sys.argv[1])
    else:
        print 'usage: http_server.py <start,stop,restart,status>'
    
