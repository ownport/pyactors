import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.exceptions import EmptyInboxException

from tests import TestGreenletActor as TestActor

def test_family():
    ''' test_generator_actors.test_family
    '''
    actor = TestActor()
    assert actor.family == pyactors.actor.AF_GENERATOR

def test_run():
    ''' test_greenlet_actors.test_run
    '''
    test_name = 'test_greenlet_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    actor = TestActor(name='Actor',logger=logger)
    actor.start()
    pyactors.joinall([actor,])

    result = []
    while True:
        try:
            result.append(actor.inbox.get())
        except EmptyInboxException:
            break
    assert len(result) == 10, result
    assert set(result) == set(['Actor:%d' % i for i in range(10)]), result

