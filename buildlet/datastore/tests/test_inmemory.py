import unittest

from ..inmemory import (
    DataValueInMemory, DataStreamInMemory, DataStoreNestableInMemory)
from .mixintestcase import (
    MixInStreamTestCase, MixInNestableAutoValueTestCase)


class TestDataValueInMemory(unittest.TestCase):

    def setUp(self):
        self.ds = DataValueInMemory()

    def test_set_get(self):
        obj = object()
        self.ds.set(obj)
        self.assertTrue(self.ds.get() is obj)


class TestDataStreamInMemory(MixInStreamTestCase, unittest.TestCase):

    def setUp(self):
        self.ds = DataStreamInMemory()


class TestDataStoreNestableInMemory(MixInNestableAutoValueTestCase,
                                    unittest.TestCase):

    def setUp(self):
        self.ds = DataStoreNestableInMemory()
