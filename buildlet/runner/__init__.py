"""
Runner classes to execute tasks.
"""

_namemodmap = dict(
    SimpleRunner='simple',
    IPythonParallelRunner='ipythonparallel',
    MultiprocessingRunner='multiprocessingpool',
)


def getrunner(classname):
    """
    Get a runner class named `classname`.
    """
    import sys
    module = 'buildlet.runner.{0}'.format(_namemodmap[classname])
    __import__(module)
    return getattr(sys.modules[module], classname)


def listrunner():
    """
    Get a list of runner class names (a list of strings).
    """
    return list(_namemodmap)


def run(classname, task, *args, **kwds):
    """
    Run `task` using runner named `classname`.

    Rest of the arguments are passed to the runner class.
    Return the instance of the used runner class.

    """
    runner = getrunner(classname)(*args, **kwds)
    runner.run(task)
    return runner
