import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.greenlets import GeventInbox
from pyactors.exceptions import EmptyInboxException

from tests import TestGreenletActor as TestActor
from tests import ParentGeneratorActor as ParentActor

def test_family():
    ''' test_greenlet_actors.test_family
    '''
    actor = TestActor()
    assert actor.family == pyactors.actor.AF_GENERATOR

def test_run_actor():
    ''' test_greenlet_actors.test_run
    '''
    test_name = 'test_greenlet_actors.test_run'
    logger = file_logger(test_name, filename='logs/%s.log' % test_name) 

    parent = ParentActor(name='Parent',logger=logger)
    child = TestActor(name='Child', logger=logger)
    parent.add_child(child)
    for i in range(10):
        child.send(test_name)
    parent.start()
    pyactors.joinall([parent,])

    result = []
    while True:
        try:
            result.append(parent.inbox.get())
        except EmptyInboxException:
            break
    assert len(result) == 10, result
    assert result == ['imap_job:%s' % test_name for _ in range(10)], result

