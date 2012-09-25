from ..task.cachedtask import BaseCachedTask
from ..datastore.inmemory import DataStoreNestableInMemory

from .test_simple import TestingTaskBase, TestSimpleTask, SimpleRootTask


class TestingCachedTask(BaseCachedTask, TestingTaskBase):
    pass


class TestCachedTask(TestSimpleTask):

    DataStoreClass = DataStoreNestableInMemory

    class TaskClass(TestingCachedTask, SimpleRootTask):

        def generate_parents(self):
            return [
                TestingCachedTask(datastore=self.datastore.get_substore(i))
                for i in range(self.num_parents)]

    def setup_task(self):
        self.ds = self.DataStoreClass()
        self.task = self.TaskClass(datastore=self.ds)

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
            self.assertEqual(self.task.get_counter(func), 2)
            self.assertEqual(ptask.get_counter(func), 2)
        self.assertEqual(self.task.get_counter('load'), 0)
        self.assertEqual(ptask.get_counter('load'), 0)

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
        self.task = self.TaskClass(datastore=self.ds)
        self.runner.run(self.task)
        self.assert_run_num(0)
        self.assert_run_num(1, 0, func='pre_run')
        self.assert_run_num(1, 0, func='post_success_run')
        self.assert_run_num(0, func='post_error_run')
