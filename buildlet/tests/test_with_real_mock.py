"""
Do :class:`TestSimpleTask` with the real mock module.
"""

import mock

# Avoid importing test case at top-level to duplicated test
from . import test_simple


class TestingTaskBaseWithRealMock(test_simple.TestingTaskBase):
    MockClass = mock.Mock


class SimpleRootTaskWithRealMock(test_simple.SimpleRootTask):
    MockClass = mock.Mock
    ParentClass = TestingTaskBaseWithRealMock


class TestSimpleTaskWithRealMock(test_simple.TestSimpleTask):
    TaskClass = SimpleRootTaskWithRealMock
