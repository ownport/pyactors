#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import re

from setuptools import setup
from pyactors import __version__ as version
from pyactors import __author__ as author

setup(
    name = "pyactors",
    version = version,
    author = re.sub(r'\s+<.*', r'', author),
    description = 'Simple implementation actors on python',
    license = "BSD",
    keywords = "actors",
    py_modules = ['pyactors'],
    classifiers = [
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],    
)
