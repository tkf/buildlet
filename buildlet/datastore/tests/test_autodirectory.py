import unittest

from ..autodirectory import DataAutoDirectory, DataAutoDirectoryWithMagic
from .mixintestcase import (
    MixInNestableTestCase, MixInWithTempDirectory,
    MixInNestableAutoValueTestCase,
)


class TestDataAutoDirectory(MixInNestableTestCase, MixInWithTempDirectory,
                            unittest.TestCase):
    dstype = DataAutoDirectory


class TestDataAutoDirectoryWithMagic(MixInNestableAutoValueTestCase,
                                     MixInWithTempDirectory,
                                     unittest.TestCase):
    dstype = DataAutoDirectoryWithMagic
