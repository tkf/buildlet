import unittest

from ..task import BaseSimpleTask
from ..task.cachedtask import BaseCachedTask
from ..runner import simple
from ..datastore.inmemory import DataStoreNestableInMemory


class ImMemoryCachedTask(BaseCachedTask, BaseSimpleTask):
    num_run = 0

    def run(self):
        self.num_run += 1

    def get_paramvalue(self):
        return self.paramvalue


class TestCachedTask(unittest.TestCase):

    runner = simple
    """Runner module."""

    class Task(ImMemoryCachedTask):

        num_parents = 3

        def generate_parents(self):
            return [
                ImMemoryCachedTask(datastore=self.datastore.get_substore(i),
                                   paramvalue=())
                for i in range(self.num_parents)]

    def assert_run_num(self, num):
        self.assertEqual(self.task.num_run, num)
        for p in self.task.get_parents():
            self.assertEqual(p.num_run, num)

    def test_simple_run(self):
        self.ds = DataStoreNestableInMemory()
        self.task = self.Task(paramvalue=(), datastore=self.ds)
        self.runner.run(self.task)
        self.assert_run_num(1)

    def test_cached_run(self):
        self.test_simple_run()
        for i in range(2):
            self.runner.run(self.task)
            self.assert_run_num(1)

    def test_invalidate_parent(self):
        self.test_simple_run()
        # Invalidate 0-th parent node cache
        ptask = self.task.get_parents()[0]
        ptask.get_hashfilestore('param').clear()
        ptask.get_hashfilestore('result').clear()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.assertEqual(self.task.num_run, 2)
        self.assertEqual(ptask.num_run, 2)
        for other in self.task.get_parents()[1:]:
            self.assertEqual(other.num_run, 1)

    def test_rerun_new_instance(self):
        self.test_simple_run()
        self.task = self.Task(paramvalue=(), datastore=self.ds)
        self.runner.run(self.task)
        self.assert_run_num(0)
