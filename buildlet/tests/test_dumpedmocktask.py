"""
Same as test_cacheabletask but mock data is dumped in datastore.

This test module serves as functional test for datastore and
basis for parallel runner (such as `multiprocessing`) testing.

"""

from ..datastore.inmemory import (
    DataStoreNestableInMemory, DataValuePickledInMemory)

# Avoid importing test case at top-level to duplicated test
from . import test_cacheabletask


class TestingDumpedMockTask(test_cacheabletask.TestingCacheableTask):

    def load_mock(self):
        store = self.datastore.get_valuestore('mock')
        if store.exists():
            self.mock = store.get()

    def pre_run(self):
        # Load mock always at the very first stage.
        self.load_mock()
        super(TestingDumpedMockTask, self).pre_run()

    def post_success_run(self):
        super(TestingDumpedMockTask, self).post_success_run()
        # Save mock at the very end:
        self.datastore.get_valuestore('mock').set(self.mock)

    def post_error_run(self, exception):
        super(TestingDumpedMockTask, self).post_error_run(exception)
        # Save mock at the very end:
        self.datastore.get_valuestore('mock').set(self.mock)


class DumpedMockRootTask(test_cacheabletask.CacheableRootTask,
                         TestingDumpedMockTask):
    pass


class TestDumpedMockTask(test_cacheabletask.TestCachedTask):

    TaskClass = DumpedMockRootTask
    ParentTaskClass = TestingDumpedMockTask

    def test_rerun_new_instance(self):
        self.test_simple_run()
        self.task = self.TaskClass(**self.get_taskclass_kwds())
        self.runner.run(self.task)

        # One more call count than TestCachedTask to count the calls in old
        # instance.
        self.assert_run_num(1, (0, 1))
        self.assert_run_num(1, (0, 1), func='load')  # except this [#]_
        self.assert_run_num(2, (1, 2), func='pre_run')
        self.assert_run_num(2, (1, 2), func='post_success_run')
        # .. [#] Because self.task.load is not called in the old instance!

        # post_error_run is never called anyway
        self.assert_run_num(0, func='post_error_run')


class DataStoreNestableCopiedInMemory(DataStoreNestableInMemory):
    # To be compatible with file-based store:
    default_valuestore_type = DataValuePickledInMemory


# # I don't need to worry about this because valuestore is not
# # used in BaseCachedTask.
# class TestCachedTaskCopiedInMemory(test_cacheabletask.TestCachedTask):
#     DataStoreClass = DataStoreNestableCopiedInMemory


class TestDumpedMockTaskCopiedInMemory(TestDumpedMockTask):
    DataStoreClass = DataStoreNestableCopiedInMemory
