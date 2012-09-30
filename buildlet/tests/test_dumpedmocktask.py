"""
Same as test_cachedtask but mock data is dumped in datastore.

This test module serves as functional test for datastore and
basis for parallel runner (such as `multiprocessing`) testing.

"""

from ..datastore.inmemory import (
    DataStoreNestableInMemory, DataValuePickledInMemory)

# Avoid importing test case at top-level to duplicated test
from . import test_cachedtask


class TestingDumpedMockTask(test_cachedtask.TestingCachedTask):

    def pre_run(self):
        # Load mock always at the very first stage.
        if 'mock' in self.datastore:
            self.mock = self.datastore.get_valuestore('mock').get()
        super(TestingDumpedMockTask, self).pre_run()

    def post_success_run(self):
        super(TestingDumpedMockTask, self).post_success_run()
        # Save mock at the very end:
        self.datastore.get_valuestore('mock').set(self.mock)


class DumpedMockRootTask(test_cachedtask.CachedRootTask,
                         TestingDumpedMockTask):
    pass


class DataStoreNestableCopiedInMemory(DataStoreNestableInMemory):
    # To be compatible with file-based store:
    default_valuestore_type = DataValuePickledInMemory


# # I don't need to worry about this because valuestore is not
# # used in BaseCachedTask.
# class TestCachedTaskCopiedInMemory(test_cachedtask.TestCachedTask):
#     DataStoreClass = DataStoreNestableCopiedInMemory


class TestDumpedMockTask(test_cachedtask.TestCachedTask):

    TaskClass = DumpedMockRootTask
    ParentTaskClass = TestingDumpedMockTask
    DataStoreClass = DataStoreNestableCopiedInMemory

    def test_rerun_new_instance(self):
        self.test_simple_run()
        self.task = self.TaskClass(**self.get_taskclass_kwds())

        for func in self.TaskClass.mock_methods:
            self.assert_run_num(0, func=func)

        def getmocks(t):
            return [t.mock] + [p.mock for p in t.get_parents()]

        def setmocks(t, mocks):
            t.mock = mocks[0]
            for (p, m) in zip(t.get_parents(), mocks[1:]):
                p.mock = m

        newmocks = getmocks(self.task)
        self.runner.run(self.task)
        loadedmocks = getmocks(self.task)
        setmocks(self.task, newmocks)

        for (nm, lm) in zip(newmocks[1:], loadedmocks[1:]):
            assert nm is lm, "Mocks for the parent task should not be loaded."
        pnum_is_zero = 0  # see TestCachedTask

        # Until `run`, the numbers are the same as in TestCachedTask
        self.assert_run_num(0, pnum_is_zero)
        self.assert_run_num(1, pnum_is_zero, func='load')
        self.assert_run_num(1, pnum_is_zero, func='pre_run')

        # New mock is not touched at all after `run`/`load`
        self.assert_run_num(0, pnum_is_zero, func='post_success_run')
        self.assert_run_num(0, pnum_is_zero, func='post_error_run')

        setmocks(self.task, loadedmocks)
        self.assert_run_num(1, pnum_is_zero)
        self.assert_run_num(0, pnum_is_zero, func='load')
        self.assert_run_num(1, pnum_is_zero, func='pre_run')

        # post_success_run mock is called in the first run and the
        # second run.
        self.assert_run_num(2, pnum_is_zero, func='post_success_run')

        self.assert_run_num(0, pnum_is_zero, func='post_error_run')
