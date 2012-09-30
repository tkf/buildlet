from ..task.cachedtask import BaseCachedTask
from ..datastore.inmemory import DataStoreNestableInMemory

# Avoid importing test case at top-level to duplicated test
from . import test_simple


class TestingCachedTask(BaseCachedTask, test_simple.TestingTaskBase):

    paramvalue = None

    def get_paramvalue(self):
        return self.paramvalue


class CachedRootTask(TestingCachedTask, test_simple.SimpleRootTask):

    def generate_parents(self):
        return [
            self.ParentTaskClass(
                MockClass=self.MockClass,
                # Only string key is supported by all nestable
                # data store types.
                datastore=self.datastore.get_substore(str(i)))
            for i in range(self.num_parents)]


class TestCachedTask(test_simple.TestSimpleTask):

    TaskClass = CachedRootTask
    ParentTaskClass = TestingCachedTask
    DataStoreClass = DataStoreNestableInMemory

    def setup_task(self):
        self.setup_datastore()
        super(TestCachedTask, self).setup_task()

    def setup_datastore(self):
        self.ds = self.DataStoreClass()

    def get_taskclass_kwds(self):
        kwds = super(TestCachedTask, self).get_taskclass_kwds()
        kwds.update(datastore=self.ds)
        return kwds

    def teardown_task(self):
        self.teardown_datastore()

    def teardown_datastore(self):
        pass

    def test_cached_run(self):
        self.test_simple_run()

        def assert_run_num_p_in_range(i, root_num_base, func):
            # Call count of `func` for root task must be increased with `i`
            root_num = root_num_base + i
            # There is no need to call `func` for parent tasks for
            # rerun, but it is OK to call them as many as root tasks.
            parent_num_range = range(root_num_base - 1, root_num + 1)
            self.assert_run_num(root_num, parent_num_range, func=func)

        for i in range(2):
            self.runner.run(self.task)
            self.assert_run_num(1)
            assert_run_num_p_in_range(i, 1, 'load')
            assert_run_num_p_in_range(i, 2, 'pre_run')
            assert_run_num_p_in_range(i, 2, 'post_success_run')
            self.assert_run_num(0, func='post_error_run')

    def test_invalidate_root(self):
        self.test_simple_run()
        self.task.invalidate_cache()
        self.runner.run(self.task)
        self.check_invalidate_root()

    def check_invalidate_root(self):
        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.assert_run_num(2, 1)
        self.assert_run_num(0, 1, func='load')
        self.assert_run_num(2, 2, func='pre_run')
        self.assert_run_num(2, 2, func='post_success_run')
        self.assert_run_num(0, func='post_error_run')

    def test_invalidate_parent(self):
        self.test_simple_run()
        # Invalidate 0-th parent node cache
        ptask = self.task.get_parents()[0]
        ptask.invalidate_cache()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.check_run_num_one_invalidated_task(ptask, 'ptask')

    def check_run_num_one_invalidated_task(self, invtask, invtaskname):
        for (expr, task) in self.iter_task_expr_val_pairs():
            num = 2 if task is invtask else 1
            self.assert_task_counter('run', num, task, expr)

        # The invalidated task
        for func in ['pre_run', 'post_success_run']:
            self.assert_task_counter(func, 2, invtask, invtaskname)
        self.assert_task_counter('load', 0, invtask, invtaskname)

        # The root task
        for func in ['pre_run', 'post_success_run']:
            self.assert_task_counter(func, 2)
        self.assert_task_counter('load', 1)

        # All tasks
        for (expr, task) in self.iter_task_expr_val_pairs():
            for func in ['pre_run', 'post_success_run']:
                self.assert_task_counter(func, (1, 2), task, expr)
            self.assert_task_counter('load', (0, 1), task, expr)

        # Finally, there should be no post_error_run call for all tasks
        for (expr, task) in self.iter_task_expr_val_pairs():
            self.assert_task_counter('post_error_run', 0, task, expr)

    def test_update_root_paramvalue(self):
        self.test_simple_run()
        self.task.paramvalue = 'new value'
        self.runner.run(self.task)
        # The effect must be the same as of :meth:`test_invalidate_root`
        self.check_invalidate_root()

    def test_update_parent_paramvalue(self):
        self.test_simple_run()
        # Update parameter of the 0-th parent node
        ptask = self.task.get_parents()[0]
        ptask.paramvalue = 'new value'
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.check_update_parent_paramvalue([self.task, ptask],
                                            ['self.task', 'ptask'])

    def check_update_parent_paramvalue(self, tasks, names):
        for (expr, task) in self.iter_task_expr_val_pairs():
            num = 2 if any(task is t for t in tasks) else 1
            self.assert_task_counter('run', num, task, expr)

        # The updated tasks and its downstreams
        for func in ['pre_run', 'post_success_run']:
            for (t, n) in zip(tasks, names):
                self.assert_task_counter(func, 2, t, n)
        for (t, n) in zip(tasks, names):
            self.assert_task_counter('load', 0, t, n)

        # All tasks
        for (expr, task) in self.iter_task_expr_val_pairs():
            for func in ['pre_run', 'post_success_run']:
                self.assert_task_counter(func, (1, 2), task, expr)
            self.assert_task_counter('load', (0, 1), task, expr)

        # Finally, there should be no post_error_run call for all tasks
        for (expr, task) in self.iter_task_expr_val_pairs():
            self.assert_task_counter('post_error_run', 0, task, expr)

    def test_rerun_new_instance(self):
        self.test_simple_run()
        self.task = self.TaskClass(**self.get_taskclass_kwds())
        self.runner.run(self.task)

        self.assert_run_num(0)

        # These function must be called once at root task.
        # There is no need to call them for parent tasks, but it's OK to call.
        self.assert_run_num(1, (0, 1), func='load')
        self.assert_run_num(1, (0, 1), func='pre_run')
        self.assert_run_num(1, (0, 1), func='post_success_run')

        # No error should be raised
        self.assert_run_num(0, func='post_error_run')
