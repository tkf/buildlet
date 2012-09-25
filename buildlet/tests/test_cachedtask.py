import unittest

from ..task import BaseSimpleTask
from ..task.cachedtask import BaseCachedTask
from ..runner import simple
from ..datastore.inmemory import DataStoreNestableInMemory


class ImMemoryCachedTask(BaseCachedTask, BaseSimpleTask):
    num_run = 0

    def run(self):
        self.num_run += 1

    def get_taskvalue(self):
        return self.taskvalue


class TestSimpleRunner(unittest.TestCase):

    runner = simple
    """Runner module."""

    class Task(ImMemoryCachedTask):

        num_parents = 3

        def generate_parents(self):
            return [
                ImMemoryCachedTask(datastore=self.datastore.get_substore(i),
                                   taskvalue=())
                for i in range(self.num_parents)]

    def assert_run_once(self):
        self.assertEqual(self.task.num_run, 1)
        for p in self.task.get_parents():
            self.assertEqual(p.num_run, 1)

    def test_simple_run(self):
        self.ds = DataStoreNestableInMemory()
        self.task = self.Task(taskvalue=(), datastore=self.ds)
        self.runner.run(self.task)
        self.assert_run_once()

    def test_cached_run(self):
        self.test_simple_run()
        for i in range(2):
            self.runner.run(self.task)
            self.assert_run_once()
