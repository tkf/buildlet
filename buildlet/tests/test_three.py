from . import test_cachedtask


class L3LeafTask(test_cachedtask.TestingCachedTask):
    pass


class L3BranchTask(test_cachedtask.CachedRootTask):
    num_parents = 2


class L3RootTask(L3BranchTask):

    def generate_parents(self):
        return [
            self.ParentTaskClass(
                MockClass=self.MockClass,
                ParentTaskClass=self.GrandParentTaskClass,
                datastore=self.datastore.get_substore(str(i)))
            for i in range(self.num_parents)]


class TestThreeLayerCachedTask(test_cachedtask.TestCachedTask):

    GrandParentTaskClass = L3LeafTask
    ParentTaskClass = L3BranchTask
    TaskClass = L3RootTask

    def get_taskclass_kwds(self):
        kwds = super(TestThreeLayerCachedTask, self).get_taskclass_kwds()
        kwds.update(GrandParentTaskClass=self.GrandParentTaskClass)
        return kwds

    def iter_task_expr_val_pairs(self):
        yield ('self.task', self.task)
        for (i, p) in enumerate(self.task.get_parents()):
            yield ('self.task.get_parents()[{0}]'.format(i), p)
            for (j, g) in enumerate(p.get_parents()):
                yield ('self.task.get_parents()[{0}].get_parents()[{1}]'
                       .format(i, j), g)

    def assert_run_num(self, root_num, parent_num=None,
                       grand_parent_num=None, func='run'):
        if grand_parent_num is None:
            if parent_num is None:
                grand_parent_num = root_num
            else:
                grand_parent_num = parent_num
        super(TestThreeLayerCachedTask, self) \
            .assert_run_num(root_num, parent_num, func=func)
        for p in self.task.get_parents():
            grand_parents = p.get_parents()
            self.assertEqual(len(grand_parents), self.task.num_parents)
            for g in grand_parents:
                self.assertEqual(g.get_counter(func), grand_parent_num)

    def test_invalidate_grand_parent(self):
        self.test_simple_run()
        # Invalidate 0-th grand parent node cache
        ptask = self.task.get_parents()[0]
        gptask = ptask.get_parents()[0]
        gptask.invalidate_cache()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)

        for (expr, task) in self.iter_task_expr_val_pairs():
            num = 2 if task is gptask else 1
            self.assert_task_counter('run', num, task, expr)

        # The invalidated grand parent task
        for func in ['pre_run', 'post_success_run']:
            self.assert_task_counter(func, 2, gptask, 'gptask')
        self.assert_task_counter('load', 0, gptask, 'gptask')

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
