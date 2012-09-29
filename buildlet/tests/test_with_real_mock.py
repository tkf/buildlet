"""
Do :class:`TestSimpleTask` with the real mock module.
"""

import mock

# Avoid importing test case at top-level to duplicated test
from . import test_simple


class TestSimpleTaskWithRealMock(test_simple.TestSimpleTask):
    MockClass = mock.Mock
