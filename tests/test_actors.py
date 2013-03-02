import sys
if '' not in sys.path:
    sys.path.append('')

import unittest
import pyactors

from pyactors.logs import file_logger

def test_actors_name():
    ''' test_actors.test_actors_name
    '''
    actor = pyactors.Actor()
    assert actor.name == 'Actor'

    actor = pyactors.Actor(name='SimpleActor')
    assert actor.name == 'SimpleActor'

def test_actors_as_str():
    ''' test_actors.test_actors_as_str
    '''
    
    actor = pyactors.Actor()
    assert str(actor) == 'Actor[%s]' % actor.address    

def test_actor_run():
    ''' test_actors.test_actor_run
    '''
    logger = file_logger(name='test_actors.test_actor_run', 
                         filename='logs/test_actors.test_actor_run.log')
    actor = pyactors.Actor(logger=logger)
    actor.start()
    actor.run()
    actor.stop()

def test_raise_error_on_start():
    ''' test_actors.test_raise_error_on_start
    '''
    class ErrorOnStartActor(pyactors.Actor):
        def on_start(self):
            self.logger.debug('on_start()')
            raise RuntimeError('Error on start')
                
    logger = file_logger(name='test_actors.test_raise_error_on_start', 
                         filename='logs/test_actors.test_raise_error_on_start.log')
    actor = ErrorOnStartActor(logger=logger)
    actor.start()
    actor.run()
    actor.stop()
