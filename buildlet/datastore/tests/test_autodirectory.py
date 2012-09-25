import unittest

from ..autodirectory import DataAutoDirectory
from .mixintestcase import MixInNestableTestCase, MixInWithTempDirectory


class TestDataAutoDirectory(MixInNestableTestCase, MixInWithTempDirectory,
                            unittest.TestCase):
    dstype = DataAutoDirectory
