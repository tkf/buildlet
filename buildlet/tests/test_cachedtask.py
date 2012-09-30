from ..task.cachedtask import BaseCachedTask
from ..datastore.inmemory import DataStoreNestableInMemory

# Avoid importing test case at top-level to duplicated test
from . import test_simple


class TestingCachedTask(BaseCachedTask, test_simple.TestingTaskBase):
    pass


class CachedRootTask(TestingCachedTask, test_simple.SimpleRootTask):

    def generate_parents(self):
        return [
            self.ParentTaskClass(
                MockClass=self.MockClass,
                # Only string key is supported by all nestable
                # data store types.
                datastore=self.datastore.get_substore(str(i)))
            for i in range(self.num_parents)]


class TestCachedTask(test_simple.TestSimpleTask):

    TaskClass = CachedRootTask
    ParentTaskClass = TestingCachedTask
    DataStoreClass = DataStoreNestableInMemory

    def setup_task(self):
        self.setup_datastore()
        super(TestCachedTask, self).setup_task()

    def setup_datastore(self):
        self.ds = self.DataStoreClass()

    def get_taskclass_kwds(self):
        kwds = super(TestCachedTask, self).get_taskclass_kwds()
        kwds.update(datastore=self.ds)
        return kwds

    def teardown_task(self):
        self.teardown_datastore()

    def teardown_datastore(self):
        pass

    def test_cached_run(self):
        self.test_simple_run()
        for i in range(2):
            self.runner.run(self.task)
            self.assert_run_num(1)
            self.assert_run_num(1 + i, 0, func='load')
            self.assert_run_num(2 + i, 1, func='pre_run')
            self.assert_run_num(2 + i, 1, func='post_success_run')
            self.assert_run_num(0, func='post_error_run')

    def test_invalidate_root(self):
        self.test_simple_run()
        self.task.invalidate_cache()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.assert_run_num(2, 1)
        self.assert_run_num(0, 1, func='load')
        self.assert_run_num(2, 2, func='pre_run')
        self.assert_run_num(2, 2, func='post_success_run')
        self.assert_run_num(0, func='post_error_run')

    def test_invalidate_parent(self):
        self.test_simple_run()
        # Invalidate 0-th parent node cache
        ptask = self.task.get_parents()[0]
        ptask.invalidate_cache()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)

        # self.task and ptask must have same call counts
        for func in ['run', 'pre_run', 'post_success_run']:
            self.assert_task_counter(func, 2)
            self.assert_task_counter(func, 2, ptask, 'ptask')
        self.assert_task_counter('load', 0)
        self.assert_task_counter('load', 0, ptask, 'ptask')

        # check other parents
        for other in self.task.get_parents()[1:]:
            self.assertEqual(other.get_counter('run'), 1)
            self.assertEqual(other.get_counter('load'), 1)
            self.assertEqual(other.get_counter('pre_run'), 2)
            self.assertEqual(other.get_counter('post_success_run'), 2)

        # finally, there should be no post_error_run call for all tasks
        self.assert_run_num(0, func='post_error_run')

    def test_rerun_new_instance(self):
        self.test_simple_run()
        self.task = self.TaskClass(**self.get_taskclass_kwds())
        self.runner.run(self.task)

        self.assert_run_num(0)

        # These function must be called once at root task.
        # There is no need to call them for parent tasks, but it's OK to call.
        self.assert_run_num(1, (0, 1), func='load')
        self.assert_run_num(1, (0, 1), func='pre_run')
        self.assert_run_num(1, (0, 1), func='post_success_run')

        # No error should be raised
        self.assert_run_num(0, func='post_error_run')
