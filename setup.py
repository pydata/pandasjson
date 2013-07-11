#!/usr/bin/env python

"""
Parts of this file were taken from the pyzmq project
(https://github.com/zeromq/pyzmq) which have been permitted for use under the
BSD license. Parts are from lxml (https://github.com/lxml/lxml)
"""

import os
import sys

# try bootstrapping setuptools if it doesn't exist
try:
    import pkg_resources
    try:
        pkg_resources.require("setuptools>=0.6c5")
    except pkg_resources.VersionConflict:
        from ez_setup import use_setuptools
        use_setuptools(version="0.6c5")
    from setuptools import setup, Command
    _have_setuptools = True
except ImportError:
    # no setuptools installed
    from distutils.core import setup, Command
    _have_setuptools = False

setuptools_kwargs = {}
if sys.version_info[0] >= 3:

    setuptools_kwargs = {'use_2to3': True,
                         'zip_safe': False,
                         'install_requires': ['python-dateutil >= 2',
                                              'pytz >= 2011k',
                                              'numpy >= 1.4'],
                         'use_2to3_exclude_fixers': ['lib2to3.fixes.fix_next',
                                                    ],
                        }
    if not _have_setuptools:
        sys.exit("need setuptools/distribute for Py3k"
            "\n$ pip install distribute")

else:
    setuptools_kwargs = {
        'install_requires': ['python-dateutil < 2',
                             'pytz >= 2011k',
                             'numpy >= 1.6'],
        'zip_safe' : False,
    }
    if not _have_setuptools:
        try:
            import numpy
            import dateutil
            setuptools_kwargs = {}
        except ImportError:
            sys.exit("install requires: 'python-dateutil < 2','numpy'."
                     "  use pip or easy_install."
                     "\n   $ pip install 'python-dateutil < 2' 'numpy'")

try:
    import numpy as np
except ImportError:
    nonumpy_msg = ("# numpy needed to finish setup.  run:\n\n"
    "    $ pip install numpy  # or easy_install numpy\n")
    sys.exit(nonumpy_msg)

if np.__version__ < '1.6.1':
    msg = "pandas requires NumPy >= 1.6 due to datetime64 dependency"
    sys.exit(msg)

from distutils.extension import Extension
from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.command.sdist import sdist

from os.path import splitext, basename, join as pjoin

DESCRIPTION = ("JSON import and export for pandas based on UltraJSON")
LONG_DESCRIPTION = """
JSON import and export based on ESN Software's UltraJSON
"""

DISTNAME = 'pandasujson'
LICENSE = 'BSD'
AUTHOR = "The PyData Development Team"
EMAIL = "pydata@googlegroups.com"
URL = "http://pandas.pydata.org"
DOWNLOAD_URL = ''
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Cython',
    'Topic :: Scientific/Engineering',
]

MAJOR = 0
MINOR = 1
MICRO = 0
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
FULLVERSION = VERSION


ujson_ext = Extension('_pandasujson',
                      depends=['ujson/lib/ultrajson.h'],
                      sources=['ujson/python/ujson.c',
                               'ujson/python/objToJSON.c',
                               'ujson/python/JSONtoObj.c',
                               'ujson/lib/ultrajsonenc.c',
                               'ujson/lib/ultrajsondec.c',
                               'datetime/np_datetime.c'
                               ],
                      include_dirs=['ujson/python', 'ujson/lib', 'datetime',
                                    np.get_include()])

extensions = [ujson_ext]

setup(name=DISTNAME,
      version=FULLVERSION,
      maintainer=AUTHOR,
      py_modules=['pandasjson'],
      ext_modules=extensions,
      maintainer_email=EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      classifiers=CLASSIFIERS,
      platforms='any',
      **setuptools_kwargs)
