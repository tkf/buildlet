"""
Runner classes to execute tasks.
"""

_namemodmap = dict(
    SimpleRunner='simple',
    IPythonParallelRunner='ipython',
    MultiprocessingRunner='multiprocessingpool',
)


def getrunner(classname):
    import sys
    module = 'buildlet.runner.{0}'.format(_namemodmap[classname])
    __import__(module)
    return getattr(sys.modules[module], classname)


def listrunner():
    return list(_namemodmap)
