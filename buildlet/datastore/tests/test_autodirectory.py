import unittest

from ..autodirectory import DataAutoDirectory, DataAutoDirectoryAutoValue
from .mixintestcase import (
    MixInNestableTestCase, MixInWithTempDirectory,
    MixInNestableAutoValueTestCase,
)


class TestDataAutoDirectory(MixInNestableTestCase, MixInWithTempDirectory,
                            unittest.TestCase):
    dstype = DataAutoDirectory


class TestDataAutoDirectoryAutoValue(MixInNestableAutoValueTestCase,
                                     MixInWithTempDirectory,
                                     unittest.TestCase):
    dstype = DataAutoDirectoryAutoValue
