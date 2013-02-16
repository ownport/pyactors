import sys
if '' not in sys.path:
    sys.path.append('')

import logging
from pyactors import network_logger

def test_network_log():
    ''' test_network_log
    '''
    logger = network_logger()
    assert isinstance(logger, logging.Logger), 'network logger creation failed'    
