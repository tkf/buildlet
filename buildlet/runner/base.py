class BaseRunner(object):

    """
    Base task runner.

    Child class must implement :meth:`run` which takes a root task
    object.

    """

    def run(self, task):
        raise NotImplementedError
