import unittest

from ..task import BaseSimpleTask
from ..runner.simple import SimpleRunner


class TestingTaskBase(BaseSimpleTask):
    state = None

    def run(self):
        self.state = 'done'


class TestSimpleRunner(unittest.TestCase):

    runnerclass = SimpleRunner

    class SimpleRunTask(TestingTaskBase):

        num_parents = 3

        def generate_parents(self):
            return [TestingTaskBase() for _ in range(self.num_parents)]

    def setUp(self):
        self.runner = self.runnerclass()

    def test_simple_run(self):
        task = self.SimpleRunTask()
        self.runner.run(task)
        self.assertEqual(task.state, 'done')
        for p in task.get_parents():
            self.assertEqual(p.state, 'done')
