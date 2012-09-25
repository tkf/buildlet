import unittest

from ..task import BaseSimpleTask
from ..runner.simple import SimpleRunner


class TestingTaskBase(BaseSimpleTask):
    num_run = 0

    def run(self):
        self.num_run += 1


class SimpleRootTask(TestingTaskBase):
    num_parents = 3

    def generate_parents(self):
        return [TestingTaskBase() for _ in range(self.num_parents)]


class TestSimpleRunner(unittest.TestCase):

    runnerclass = SimpleRunner
    TaskClass = SimpleRootTask

    def setUp(self):
        self.runner = self.runnerclass()
        self.task = self.TaskClass()

    def assert_run_num(self, root_num, parent_num=None):
        if parent_num is None:
            parent_num = root_num
        self.assertEqual(self.task.num_run, root_num)
        parents = self.task.get_parents()
        self.assertEqual(len(parents), self.task.num_parents)
        for p in parents:
            self.assertEqual(p.num_run, parent_num)

    def test_simple_run(self):
        self.assert_run_num(0)
        self.runner.run(self.task)
        self.assert_run_num(1)
