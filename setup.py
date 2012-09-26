try:
    from setuptools import setup
except:
    from distutils.core import setup
import sys

import buildlet

setup_kwds = {}

if sys.version_info[0] >= 3:
    setup_kwds['use_2to3'] = True

setup(
    name='buildlet',
    version=buildlet.__version__,
    packages=['buildlet',
              'buildlet.runner',
              'buildlet.tests',
             ],
    author=buildlet.__author__,
    author_email='aka.tkf@gmail.com',
    url='https://github.com/tkf/buildlet',
    license=buildlet.__license__,
    description='buildlet - build tool like functionality as a Python module',
    long_description=buildlet.__doc__,
    keywords='build, task, dependency',
    classifiers=[
        "Development Status :: 3 - Alpha",
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    **setup_kwds
)
