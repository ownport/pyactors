import sys
if '' not in sys.path:
    sys.path.append('')

import time
import logging
import unittest

from pyactors.generator import GeneratorActor
from pyactors.forked import ForkedGeneratorActor
from pyactors.forked import ForkedGreenletActor
from pyactors.exceptions import EmptyInboxException

_logger = logging.getLogger('test_forked_actors')

class ForkedGenActor(ForkedGeneratorActor):
    ''' Forked Generator Actor
    '''
    def __init__(self):
        super(ForkedGenActor, self).__init__()
        self.result = 0
    
    def loop(self):
        for i in xrange(10):
            if self.processing:
                self.result += i
                yield
            else:
                break
        self.stop()


