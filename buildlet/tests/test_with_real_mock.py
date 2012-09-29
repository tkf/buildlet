"""
Test with the real mock module.
"""

import mock

# Avoid importing test case at top-level to duplicated test
from . import test_simple
from . import test_cachedtask
from . import test_cachedtask_directory


class TestSimpleTaskWithRealMock(test_simple.TestSimpleTask):
    MockClass = mock.Mock


class TestCachedTaskWithRealMock(test_cachedtask.TestCachedTask):
    MockClass = mock.Mock


class TestCachedTaskDirectoryAndWithRealMock(
        test_cachedtask_directory.TestCachedTaskDirectory):
    MockClass = mock.Mock
