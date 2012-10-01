"""
Test with three-level task tree.

The task tree is like this (when ``num_parents = 2``):

  * ``L3RootTask()`` (``self.task``)

    * ``L3BranchTask()`` (``ptask`` / "parent task")

      * ``L3LeafTask()`` (``gptask`` / "grand parent task")
      * ``L3LeafTask()``

    * ``L3BranchTask()``

      * ``L3LeafTask()``
      * ``L3LeafTask()``

"""


from . import test_cacheabletask


class L3LeafTask(test_cacheabletask.TestingCachedTask):
    pass


class L3BranchTask(test_cacheabletask.CachedRootTask):
    num_parents = 2


class L3RootTask(L3BranchTask):

    def generate_parents(self):
        return [
            self.ParentTaskClass(
                MockClass=self.MockClass,
                ParentTaskClass=self.GrandParentTaskClass,
                datastore=self.datastore.get_substore(str(i)))
            for i in range(self.num_parents)]


class TestThreeLayerCachedTask(test_cacheabletask.TestCachedTask):

    GrandParentTaskClass = L3LeafTask
    ParentTaskClass = L3BranchTask
    TaskClass = L3RootTask

    def get_taskclass_kwds(self):
        kwds = super(TestThreeLayerCachedTask, self).get_taskclass_kwds()
        kwds.update(GrandParentTaskClass=self.GrandParentTaskClass)
        return kwds

    def iter_task_expr_val_pairs(self, levels=(0, 1, 2)):
        for pair in super(TestThreeLayerCachedTask, self) \
                        .iter_task_expr_val_pairs(levels):
            yield pair
        if 2 in levels:
            for (i, p) in enumerate(self.task.get_parents()):
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
            self.assertEqual(len(grand_parents), p.num_parents)
        for (expr, task) in self.iter_task_expr_val_pairs((2,)):
            self.assert_task_counter(func, grand_parent_num, task, expr)

    def test_invalidate_grand_parent(self):
        self.test_simple_run()
        # Invalidate 0-th grand parent node cache
        gptask = self.task.get_parents()[0].get_parents()[0]
        gptask.invalidate_cache()
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.check_run_num_one_invalidated_task(gptask, 'gptask')

    def test_update_grand_parent_paramvalue(self):
        self.test_simple_run()
        # Update parameter of the 0-th grand parent node
        ptask = self.task.get_parents()[0]
        gptask = ptask.get_parents()[0]
        gptask.paramvalue = 'new value'
        self.runner.run(self.task)

        self.assertRaises(AssertionError, self.assert_run_num, 1)
        self.check_update_parent_paramvalue([self.task, ptask, gptask],
                                            ['self.task', 'ptask', 'gptask'])
