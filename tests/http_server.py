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

from packages import bottle
from packages.bottle import request

app = bottle.app()

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


@app.route('/', method=['GET'])
def index():
    ''' index
    '''
    return get_request_dict() 

bottle.run(app=app, host='127.0.0.1', port=8800, reloader=True)

