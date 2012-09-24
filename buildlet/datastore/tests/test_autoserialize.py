import unittest

from ..autoserialize import DataValuePickle, DataValueJSON, DataValueYAML
from .mixintestcase import MixInValueTestCase, MixInWithTempFile


class TestDataValuePickle(MixInValueTestCase, MixInWithTempFile,
                          unittest.TestCase):
    dstype = DataValuePickle


class TestDataValueJSON(MixInValueTestCase, MixInWithTempFile,
                        unittest.TestCase):
    dstype = DataValueJSON


class TestDataValueYAML(MixInValueTestCase, MixInWithTempFile,
                        unittest.TestCase):
    dstype = DataValueYAML
