import unittest

from ..task import BaseSimpleTask
from ..runner.simple import SimpleRunner


class TestingTaskBase(BaseSimpleTask):

    def __init__(self, *args, **kwds):
        super(TestingTaskBase, self).__init__(*args, **kwds)
        self._counter = {}

    def inc_counter(self, key):
        self.get_counter(key)
        self._counter[key] += 1

    def get_counter(self, key):
        return self._counter.setdefault(key, 0)

    def run(self):
        self.inc_counter('run')


class SimpleRootTask(TestingTaskBase):
    num_parents = 3

    def generate_parents(self):
        return [TestingTaskBase() for _ in range(self.num_parents)]


class TestSimpleTask(unittest.TestCase):

    RunnerClass = SimpleRunner
    TaskClass = SimpleRootTask

    def setUp(self):
        self.setup_runner()
        self.setup_task()

    def setup_runner(self):
        self.runner = self.RunnerClass()

    def setup_task(self):
        self.task = self.TaskClass()

    def assert_run_num(self, root_num, parent_num=None):
        if parent_num is None:
            parent_num = root_num
        self.assertEqual(self.task.get_counter('run'), root_num)
        parents = self.task.get_parents()
        self.assertEqual(len(parents), self.task.num_parents)
        for p in parents:
            self.assertEqual(p.get_counter('run'), parent_num)

    def test_simple_run(self):
        self.assert_run_num(0)
        self.runner.run(self.task)
        self.assert_run_num(1)
