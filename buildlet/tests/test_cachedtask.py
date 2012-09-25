from ..task.cachedtask import BaseCachedTask
from ..datastore.inmemory import DataStoreNestableInMemory

from .test_simple import TestingTaskBase, TestSimpleRunner, SimpleRootTask


class ImMemoryCachedTask(BaseCachedTask, TestingTaskBase):
    pass


class TestCachedTask(TestSimpleRunner):

    class TaskClass(ImMemoryCachedTask, SimpleRootTask):

        def generate_parents(self):
            return [
                ImMemoryCachedTask(datastore=self.datastore.get_substore(i))
                for i in range(self.num_parents)]

    def setup_task(self):
        self.ds = DataStoreNestableInMemory()
        self.task = self.TaskClass(datastore=self.ds)

    def test_cached_run(self):
        self.test_simple_run()
        for i in range(2):
            self.runner.run(self.task)
            self.assert_run_num(1)

    def test_invalidate_root(self):
        self.test_simple_run()
        self.task.invalidate_cache()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.assert_run_num(2, 1)

    def test_invalidate_parent(self):
        self.test_simple_run()
        # Invalidate 0-th parent node cache
        ptask = self.task.get_parents()[0]
        ptask.invalidate_cache()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.assertEqual(self.task.num_run, 2)
        self.assertEqual(ptask.num_run, 2)
        for other in self.task.get_parents()[1:]:
            self.assertEqual(other.num_run, 1)

    def test_rerun_new_instance(self):
        self.test_simple_run()
        self.task = self.TaskClass(datastore=self.ds)
        self.runner.run(self.task)
        self.assert_run_num(0)
