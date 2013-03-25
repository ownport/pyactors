import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors
from pyactors.logs import file_logger
from pyactors.exceptions import EmptyInboxException

from tests import ParentGeneratorActor as ParentActor
from tests import TestThreadedGeneratorActor as TestActor

def test_run():
    ''' test_threaded_actors.test_run
    '''
    test_name = 'test_threaded_actors.test_run'
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
    assert result == [test_name for _ in range(10)], result

