"""
Tasks cached on data store.
"""

import operator

from .base import BaseTask


class BaseCachedTask(BaseTask):

    """
    Base task class for automatic dependency check based on cached result.

    This class store hashes representing "state" of this task.
    These hashes are used to determine when to load cached data
    or run task again.

    There are there "states" for one task:

    `paramvalue`
       Parameters given to the task.  Using this, you can re-run task
       when changing the parameter given to the task.
       You can change this by :meth:`get_paramvalue`.

    `resultvalue`
       Result of the task.  If the result of this task is predictable
       by its parameter (i.e., `paramvalue`), you do not care about
       this value.  If the result is `unpredictable`, this value is
       useful. You can change this by :meth:`get_returnvalue`.

    `parent_hashes`
       A (possibly empty) tuple of parent task `resulthash` (see
       below).  User of this class does not need to care about this
       value, as this class automatically takes care of it.

    Based on these values, `paramhash` and `resulthash` are
    calculated as follows.::

        paramhash  = hash((paramvalue, parent_hashes))
        resulthash = hash((paramvalue, parent_hashes, resultvalue))

    When the cache on :attr:`datastore` is found, cached `paramhash`
    is compared with calculated one (by :meth:`is_finished`).  If
    they differ, this task will be run again.  Otherwise, data will be
    loaded from :attr:`datastore`.

    """

    datastore = None
    """
    Data store instance.  Child class **must** set this attribute.
    """

    def is_finished(self):
        current = self.get_hash('param')
        cached = self.get_cached_hash('param')
        return current is not None and \
            cached is not None and \
            current == cached

    #----------------------------------------------------------------------
    # Task value calculation
    #----------------------------------------------------------------------

    def get_paramvalue(self):
        """
        Return a hash-able object which represents parameter for this task.

        Note that this value should not depend on the result
        of the :meth:`run` function.  Use :meth:`get_resultvalue`
        for that purpose.

        It is better if this value provides enough information to get
        the same result.  In this case, you don't need to implement
        :meth:`get_resultvalue`.  For example, you can include file
        hash of your source code in `paramvalue`.

        """
        return None

    def get_resultvalue(self):
        """
        Return a hash-able object which represents result of this task.

        Define this method to return an object which can identify the
        result of this task.  For example, if the result differs for
        every run, downstream tasks must be run again when this task
        is run after them.  This method is needed to detect when to
        re-run downstream tasks.

        """
        return None

    #----------------------------------------------------------------------
    # Hash calculation
    #----------------------------------------------------------------------

    @staticmethod
    def _check_hashname(hashname):
        if hashname not in ('param', 'result'):
            raise ValueError(
                "`hashname` must be 'param' or 'result. '"
                "given value is '{0}'.".format(hashname))

    def get_hash(self, hashname):
        """
        Get a hash based on `paramvalue`, `parent_hashes` (and `resultvalue`).
        """
        self._check_hashname(hashname)
        if not self.is_parent_cacheable():
            return None
        parent_hashes = self.get_parent_hashes()
        if any(h is None for h in parent_hashes):
            return None
        paramvalue = self.get_paramvalue()
        value = (paramvalue, parent_hashes)
        if hashname == 'result':
            value += (self.get_resultvalue(),)
        # TODO: This relies on that `hash` returns the same value for every
        #       run.  Does it hold always?  Find out!
        return hash(value)

    def get_parent_hashes(self, hashname='result'):
        """
        Get a tuple of of parent hashes.
        """
        get = operator.methodcaller('get_cached_hash', hashname=hashname)
        return tuple(map(get, self.get_parents()))

    def is_parent_cacheable(self):
        return all(isinstance(p, BaseCachedTask) for p in self.get_parents())

    #----------------------------------------------------------------------
    # Hash caching
    #----------------------------------------------------------------------

    def get_metafilestore(self, key):
        return self.datastore.get_metastore().get_filestore(key)

    def get_hashfilestore(self, hashname):
        self._check_hashname(hashname)
        return self.get_metafilestore(hashname + 'hash')

    def get_cached_hash(self, hashname):
        store = self.get_hashfilestore(hashname)
        if not store.exists():
            return None
        with store.open() as f:
            return int(f.read())

    def set_cached_hash(self, hashname):
        store = self.get_hashfilestore(hashname)
        taskhash = self.get_hash(hashname)
        with store.open('w') as f:
            f.write(str(taskhash))

    def post_success_run(self):
        self.set_cached_hash('result')
        self.set_cached_hash('param')
        super(BaseCachedTask, self).post_success_run()

    def invalidate_cache(self):
        """
        Invalidate cache of this task.
        """
        self.get_hashfilestore('result').clear()
        self.get_hashfilestore('param').clear()
