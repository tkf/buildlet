import unittest

from ..utils.mocklet import Mock
from ..task import BaseSimpleTask
from ..runner.simple import SimpleRunner


class TestingTaskBase(BaseSimpleTask):

    mock_methods = [
        'run', 'load', 'pre_run', 'post_success_run', 'post_error_run']

    def __init__(self, MockClass, ParentTaskClass=None, *args, **kwds):
        self.MockClass = MockClass
        self.ParentTaskClass = ParentTaskClass
        super(TestingTaskBase, self).__init__(*args, **kwds)

        # As these methods can be inherited from other classes, use
        # mock "indirectly" here (don't do ``self.run = mock.Mock()``).
        self.mock = {}
        for func in self.mock_methods:
            self.mock[func] = self.MockClass()

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
        return [self.ParentTaskClass(MockClass=self.MockClass)
                for _ in range(self.num_parents)]


class TestSimpleTask(unittest.TestCase):

    RunnerClass = SimpleRunner
    TaskClass = SimpleRootTask
    ParentTaskClass = TestingTaskBase
    MockClass = Mock

    def setUp(self):
        self.setup_runner()
        self.setup_task()

    def setup_runner(self):
        self.runner = self.RunnerClass()

    def setup_task(self):
        self.task = self.TaskClass(**self.get_taskclass_kwds())

    def get_taskclass_kwds(self):
        return dict(
            MockClass=self.MockClass,
            ParentTaskClass=self.ParentTaskClass,
        )

    def tearDown(self):
        self.teardown_runner()
        self.teardown_task()

    def teardown_runner(self):
        pass

    def teardown_task(self):
        pass

    def assert_task_counter(self, func, num, task=None, taskname=None):
        if task is None:
            task = self.task
            taskname = 'self.task'
        if taskname is None:
            taskname = repr(task)
        if isinstance(num, int):
            num = (num,)
        real_num = task.get_counter(func)
        self.assertTrue(
            real_num in num,
            "{0}.{1} is expected to be called {2} times but called {3} times"
            .format(taskname, func, "or ".join(map(str, num)), real_num))

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

        # Do `assert call_args_list == ((exception,), {})`,
        # but it should work with `exception` coming from
        # other process.
        call_args_list = self.task.mock['post_error_run'].call_args_list
        self.assertEqual(len(call_args_list), 1)
        self.assertEqual(len(call_args_list[0]), 2)
        self.assertEqual(len(call_args_list[0][0]), 1)
        self.assertEqual(call_args_list[0][1], {})
        should_be_exception = call_args_list[0][0][0]
        assert isinstance(should_be_exception, ValueError)
        self.assertEqual(should_be_exception.message, exception.message)
