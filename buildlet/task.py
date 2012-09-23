class TaskBase(object):

    """
    Task base class with empty method definitions.
    """

    def get_parents(self):
        """
        Return a list of parent task instances.

        To access parent data in :meth:`run`, you need to store
        parent node in attributes.

        """
        return []

    def load(self):
        """
        Load computed result from data store.

        This function is called instead of :meth:`run` when
        :meth:`is_finished` returns True.

        """

    def run(self):
        """
        Run task.
        """

    def pre_run(self):
        """
        Run by task runner before anything else.
        """

    def post_run(self):
        """
        Run by task runner after the actual task, even if it failed.
        """

    def is_finished(self):
        """
        Return True when the task is finished and loadable by :meth:`load`.
        """
        return False


class SimpleTaskBase(TaskBase):

    """
    Task base class with predefined methods.

    :meth:`__init__`
        Store all keyword arguments as attributes.

    :meth:`get_parents`
        Store what :meth:`generate_parents` returns in cache
        and use it after the first call.

    """

    _parents = None

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def generate_parents(self):
        """
        Return a list of parent task instances.
        """
        return []

    def get_parents(self):
        """
        Memoized version of :meth:`generate_parents`.
        """
        if self._parents is None:
            self._parents = self.generate_parents()
        return self._parents
