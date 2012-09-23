from distutils.core import setup

import buildlet

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
)
