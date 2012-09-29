import unittest

from ..directory import DataFile, DataDirectory, DataDirectoryWithMagic
from .mixintestcase import (
    MixInStreamTestCase, MixInNestableTestCase, MixInNestableAutoValueTestCase,
    MixInWithTempFile, MixInWithTempDirectory,
)


class TestDataFile(MixInStreamTestCase, MixInWithTempFile, unittest.TestCase):
    dstype = DataFile


class TestDataDirectory(MixInNestableTestCase, MixInWithTempDirectory,
                        unittest.TestCase):
    dstype = DataDirectory


class TestDataDirectoryWithMagic(MixInNestableAutoValueTestCase,
                                 MixInWithTempDirectory,
                                 unittest.TestCase):
    dstype = DataDirectoryWithMagic
