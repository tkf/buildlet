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

    def test_simple_run(self):
        ds = DataStoreNestableInMemory()
        task = self.Task(taskvalue=(), datastore=ds)
        self.runner.run(task)
        self.assertEqual(task.num_run, 1)
        for p in task.get_parents():
            self.assertEqual(p.num_run, 1)
