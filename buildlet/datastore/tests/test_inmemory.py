import unittest

from ..inmemory import (
    DataValueInMemory, DataStreamInMemory, DataStoreNestableInMemory)
from .mixintestcase import (
    MixInValueTestCase, MixInStreamTestCase, MixInNestableAutoValueTestCase)


class TestDataValueInMemory(MixInValueTestCase, unittest.TestCase):

    dstype = DataValueInMemory

    def test_set_get_singleton(self):
        obj = object()
        self.ds.set(obj)
        self.assertTrue(self.ds.get() is obj)


class TestDataStreamInMemory(MixInStreamTestCase, unittest.TestCase):
    dstype = DataStreamInMemory


class TestDataStoreNestableInMemory(MixInNestableAutoValueTestCase,
                                    unittest.TestCase):
    dstype = DataStoreNestableInMemory
