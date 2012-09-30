import os
import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup

import buildlet


def find_packages():
    packages = []
    for (dir, subdirs, files) in os.walk('buildlet'):
        package = dir.replace(os.path.sep, '.')
        if '__init__.py' in files:
            packages.append(package)
    return packages


setup_kwds = {}

if sys.version_info[0] >= 3:
    setup_kwds['use_2to3'] = True

setup(
    name='buildlet',
    version=buildlet.__version__,
    packages=find_packages(),
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
