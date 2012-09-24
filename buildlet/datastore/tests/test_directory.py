import unittest

from ..directory import DataFile, DataDirectory
from .mixintestcase import (
    MixInStreamTestCase, MixInNestableTestCase,
    MixInWithTempFile, MixInWithTempDirectory,
)


class TestDataFile(MixInStreamTestCase, MixInWithTempFile, unittest.TestCase):
    dstype = DataFile


class TestDataDirectory(MixInNestableTestCase, MixInWithTempDirectory,
                        unittest.TestCase):
    dstype = DataDirectory
