import sys
if '' not in sys.path:
    sys.path.append('')

import pyactors

def test_joinall():
    
    try:
        pyactors.joinall('actor')
    except RuntimeError:
        pass
    
    pyactors.joinall([pyactors.actor.Actor(),])
