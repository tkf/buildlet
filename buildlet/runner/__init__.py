"""
Utility functions to execute tasks.
"""

_namemodmap = dict(
    SimpleRunner='simple',
    IPythonParallelRunner='ipythonparallel',
    MultiprocessingRunner='multiprocessingpool',
)


def getrunner(runnername):
    """
    Get a runner class named `runnername`.

    >>> getrunner('SimpleRunner')
    <class 'buildlet.runner.simple.SimpleRunner'>

    """
    import sys
    module = 'buildlet.runner.{0}'.format(_namemodmap[runnername])
    __import__(module)
    return getattr(sys.modules[module], runnername)


def listrunner():
    """
    Get a list of runner class names (a list of strings).

    Currently defined runners:

    >>> sorted(listrunner())
    ['IPythonParallelRunner', 'MultiprocessingRunner', 'SimpleRunner']

    """
    return list(_namemodmap)


def run(runnername, task, *args, **kwds):
    """
    Run `task` using runner named `runnername`.

    Rest of the arguments are passed to the runner class.
    Return the instance of the used runner class.

    Usage::

        runner = run('SimpleRunner', task)

    """
    runner = getrunner(runnername)(*args, **kwds)
    runner.run(task)
    return runner
