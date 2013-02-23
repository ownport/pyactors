import sys
if '' not in sys.path:
    sys.path.append('')

import logging
from pyactors import Actor
from pyactors.logs import network_logger

def test_network_log():
    ''' test_log.test_network_log
    '''
    logger = network_logger()
    assert isinstance(logger, logging.Logger), 'network logger creation failed'    

def test_actor_logger():
    ''' test_log.test_actor_logger
    '''
    logger = logging.getLogger('test_log.test_actor_logger')
    actor = Actor(name='actor-with-logger', logger=logger)
    assert isinstance(actor.logger, logging.Logger), 'actor\'s logger creation failed'    
    
