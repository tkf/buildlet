import unittest

from buildlet.task import BaseSimpleTask
from buildlet.runner import simple


class TestingTaskBase(BaseSimpleTask):
    state = None

    def run(self):
        self.state = 'done'


class TestSimpleRunner(unittest.TestCase):

    runner = simple
    """Runner module."""

    class SimpleRunTask(TestingTaskBase):

        num_parents = 3

        def generate_parents(self):
            return [TestingTaskBase() for _ in range(self.num_parents)]

    def test_simple_run(self):
        task = self.SimpleRunTask()
        self.runner.run(task)
        self.assertEqual(task.state, 'done')
        for p in task.get_parents():
            self.assertEqual(p.state, 'done')
