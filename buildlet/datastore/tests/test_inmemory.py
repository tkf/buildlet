import unittest

from ..inmemory import (
    DataValueInMemory, DataValuePickledInMemory, DataStreamInMemory,
    DataStoreNestableInMemory, DataStoreNestableInMemoryAutoValue)
from .mixintestcase import (
    MixInValueTestCase, MixInStreamTestCase,
    MixInNestableTestCase, MixInNestableAutoValueTestCase)


class TestDataValueInMemory(MixInValueTestCase, unittest.TestCase):

    dstype = DataValueInMemory

    def test_set_get_singleton(self):
        obj = object()
        self.ds.set(obj)
        self.assertTrue(self.ds.get() is obj)


class TestDataValuePickledInMemory(MixInValueTestCase, unittest.TestCase):
    dstype = DataValuePickledInMemory


class TestDataStreamInMemory(MixInStreamTestCase, unittest.TestCase):
    dstype = DataStreamInMemory


class TestDataStoreNestableInMemory(MixInNestableTestCase,
                                    unittest.TestCase):
    dstype = DataStoreNestableInMemory


class TestDataStoreNestableInMemoryAutoValue(MixInNestableAutoValueTestCase,
                                             unittest.TestCase):
    dstype = DataStoreNestableInMemoryAutoValue
