import unittest

import mock

from ..task import BaseSimpleTask
from ..runner.simple import SimpleRunner


class TestingTaskBase(BaseSimpleTask):

    def __init__(self, *args, **kwds):
        super(TestingTaskBase, self).__init__(*args, **kwds)

        # As these methods can be inherited from other classes, use
        # mock "indirectly" here (don't do ``self.run = mock.Mock()``).
        self.mock = {}
        for func in ['run', 'pre_run', 'post_success_run', 'post_error_run']:
            self.mock[func] = mock.Mock()

    def get_counter(self, key):
        return self.mock[key].call_count

    def run(self):
        self.mock['run']()

    def pre_run(self):
        self.mock['pre_run']()

    def post_success_run(self):
        self.mock['post_success_run']()

    def post_error_run(self, exception):
        self.mock['post_error_run'](exception=exception)


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

    def assert_run_num(self, root_num, parent_num=None, func='run'):
        if parent_num is None:
            parent_num = root_num
        self.assertEqual(self.task.get_counter(func), root_num)
        parents = self.task.get_parents()
        self.assertEqual(len(parents), self.task.num_parents)
        for p in parents:
            self.assertEqual(p.get_counter(func), parent_num)

    def test_simple_run(self):
        self.assert_run_num(0)
        self.runner.run(self.task)
        self.assert_run_num(1)
        self.assert_run_num(1, func='pre_run')
        self.assert_run_num(1, func='post_success_run')
        self.assert_run_num(0, func='post_error_run')

    def test_post_error_run(self):
        exception = ValueError('Error for test')
        self.task.mock['run'].side_effect = exception
        self.assertRaises(ValueError, self.runner.run, self.task)
        self.assert_run_num(1)
        self.assert_run_num(1, func='pre_run')
        self.assert_run_num(0, 1, func='post_success_run')
        self.assert_run_num(1, 0, func='post_error_run')
        self.task.mock['post_error_run'] \
            .assert_called_once_with(exception=exception)
