import unittest

from ..directory import DataFile, DataDirectory, DataDirectoryAutoValue
from .mixintestcase import (
    MixInStreamTestCase, MixInNestableTestCase, MixInNestableAutoValueTestCase,
    MixInWithTempFile, MixInWithTempDirectory,
)


class TestDataFile(MixInStreamTestCase, MixInWithTempFile, unittest.TestCase):
    dstype = DataFile


class TestDataDirectory(MixInNestableTestCase, MixInWithTempDirectory,
                        unittest.TestCase):
    dstype = DataDirectory


class TestDataDirectoryAutoValue(MixInNestableAutoValueTestCase,
                                 MixInWithTempDirectory,
                                 unittest.TestCase):
    dstype = DataDirectoryAutoValue
