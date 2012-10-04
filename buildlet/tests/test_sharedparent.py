"""
Test task tree with shared node.

::

  Root -+-----> Mid1 --+
         \              \
          `---> Mid2 ----+---> Shared

"""

from . import test_simple


class FixedParentTask(test_simple.TestingTaskBase):

    def generate_parents(self):
        return self.parents


class SharedParentRootTask(test_simple.SimpleRootTask):
    num_parents = 2

    def generate_parents(self):
        shared = self.GrandParentTaskClass(MockClass=self.MockClass)
        return [self.ParentTaskClass(parents=[shared],
                                     MockClass=self.MockClass)
                for _ in range(self.num_parents)]


class TestSharedParent(test_simple.TestSimpleTask):

    GrandParentTaskClass = test_simple.TestingTaskBase
    ParentTaskClass = FixedParentTask
    TaskClass = SharedParentRootTask

    def get_taskclass_kwds(self):
        kwds = super(TestSharedParent, self).get_taskclass_kwds()
        kwds.update(GrandParentTaskClass=self.GrandParentTaskClass)
        return kwds
