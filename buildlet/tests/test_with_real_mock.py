"""
Test with the real mock module.
"""

import mock

# Avoid importing test case at top-level to duplicated test
from . import test_simple
from . import test_cacheabletask
from . import test_cacheabletask_directory


class TestSimpleTaskWithRealMock(test_simple.TestSimpleTask):
    MockClass = mock.Mock


class TestCacheableTaskWithRealMock(test_cacheabletask.TestCacheableTask):
    MockClass = mock.Mock


class TestCacheableTaskDirectoryAndWithRealMock(
        test_cacheabletask_directory.TestCachedTaskDirectory):
    MockClass = mock.Mock
