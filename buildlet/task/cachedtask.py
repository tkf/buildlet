"""
Tasks cached on data store.
"""

from .base import BaseTask


class BaseCachedTask(BaseTask):

    datastore = None
    """
    Data store instance.  Child class **must** set this attribute.
    """

    def is_finished(self):
        current = self.get_taskhash()
        cached = self.get_cached_taskhash()
        return current is not None and \
            cached is not None and \
            current == cached

    def get_taskvalue(self):
        """
        Return a hash-able object which can identify this task.

        Note that this value should not depend on the result
        of the :meth:`run` function.  However, this value should
        provide enough information to get the same result.

        """
        raise NotImplementedError

    def get_taskhash(self):
        if not self.is_parent_cacheable():
            return None
        parent_hashes = self.get_parent_hashes()
        if any(h is None for h in parent_hashes):
            return None
        taskvalue = self.get_taskvalue()
        # TODO: This relies on that `hash` returns the same value for every
        #       run.  Does it hold always?  Find out!
        return hash((taskvalue, tuple(parent_hashes)))

    def get_parent_hashes(self):
        return map(BaseCachedTask.get_cached_taskhash, self.get_parents())

    def is_parent_cacheable(self):
        return all(isinstance(p, BaseCachedTask) for p in self.get_parents())

    def get_taskhashstore(self):
        return self.datastore.get_metastore().get_filestore('taskhash')

    def get_cached_taskhash(self):
        store = self.get_taskhashstore()
        if not store.exists():
            return None
        with store.open() as f:
            return int(f.read())

    def set_cached_taskhash(self):
        taskhash = self.get_taskhash()
        with self.get_taskhashstore().open('w') as f:
            f.write(str(taskhash))

    def post_run(self):
        # TODO: check if task raises an error and do NOT set cache if so.
        self.set_cached_taskhash()
        super(BaseCachedTask, self).post_run()
