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

import logging

def file_logger(name, filename):
    ''' returns file logger
    '''
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(filename)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    return logger

def network_logger( name=__name__, level=logging.DEBUG,
                    host='127.0.0.1', port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
    ''' return network logger
    '''
    logger = logging.getLogger(name)
    logger.setLevel(level)
    socketHandler = logging.handlers.SocketHandler(host, port)
    formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')
    socketHandler.setFormatter(formatter)
    logger.addHandler(socketHandler)
    return logger

