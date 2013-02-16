#!/usr/bin/env python
#
#   loging console
#
__author__ = 'Andrey Usov <https://github.com/ownport/pyactors>'
__version__ = '0.2'
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

import struct
import cPickle
import logging
import logging.handlers

LOG_FIELDS_FILTER = [
    'client_ip',
    'threadName',
    'name',
    'thread',
    'relativeCreated',
    'process',
    'args',
    'module',
    'funcName',
    'levelno',
    'processName',
    'created',
    'msecs',
    'msg',
    'exc_info',
    'exc_text',
    'pathname',
    'filename',
    'levelname',
    'lineno',    
]

LOG_CONSOLE_IP_ADDRESS = '127.0.0.1'
LOG_CONSOLE_PORT = logging.handlers.DEFAULT_TCP_LOGGING_PORT

def handle(socket, address):
    ''' handle request to log
    '''
    chunk = socket.recv(4)
    if len(chunk) < 4:
        return
    slen = struct.unpack(">L", chunk)[0]
    chunk = socket.recv(slen)
    while len(chunk) < slen:
        chunk = chunk + socket.recv(slen - len(chunk))
    log_record = cPickle.loads(chunk)
    log_record['client_ip'] = address
    print log_record

def main():
    ''' main
    '''
    from gevent.pool import Pool
    from gevent.server import StreamServer

    pool = Pool(20)
    server = StreamServer((LOG_CONSOLE_IP_ADDRESS, LOG_CONSOLE_PORT), handle, spawn=pool)
    print 'Logging console opened, %s:%s' % (LOG_CONSOLE_IP_ADDRESS, LOG_CONSOLE_PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Logging console closed'

if __name__ == '__main__':
    main()
    
