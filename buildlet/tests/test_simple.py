import unittest

import mock

from ..task import BaseSimpleTask
from ..runner.simple import SimpleRunner


class TestingTaskBase(BaseSimpleTask):

    mock_methods = [
        'run', 'load', 'pre_run', 'post_success_run', 'post_error_run']

    def __init__(self, *args, **kwds):
        super(TestingTaskBase, self).__init__(*args, **kwds)

        # As these methods can be inherited from other classes, use
        # mock "indirectly" here (don't do ``self.run = mock.Mock()``).
        self.mock = {}
        for func in self.mock_methods:
            self.mock[func] = mock.Mock()

    def get_counter(self, key):
        return self.mock[key].call_count

    @classmethod
    def define_mocked_method(cls, key):
        def method(self, *args, **kwds):
            return self.mock[key](*args, **kwds)
        setattr(cls, key, method)

    @classmethod
    def define_all_mocked_methods(cls):
        for func in cls.mock_methods:
            cls.define_mocked_method(func)


TestingTaskBase.define_all_mocked_methods()


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

    def tearDown(self):
        self.teardown_runner()
        self.teardown_task()

    def teardown_runner(self):
        pass

    def teardown_task(self):
        pass

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
        self.assert_run_num(0, func='load')
        self.assert_run_num(1, func='pre_run')
        self.assert_run_num(1, func='post_success_run')
        self.assert_run_num(0, func='post_error_run')

    def test_post_error_run(self):
        exception = ValueError('Error for test')
        self.task.mock['run'].side_effect = exception
        self.assertRaises(ValueError, self.runner.run, self.task)
        self.assert_run_num(1)
        self.assert_run_num(0, func='load')
        self.assert_run_num(1, func='pre_run')
        self.assert_run_num(0, 1, func='post_success_run')
        self.assert_run_num(1, 0, func='post_error_run')
        self.task.mock['post_error_run'].assert_called_once_with(exception)
