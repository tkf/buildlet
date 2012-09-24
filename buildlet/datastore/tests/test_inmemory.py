import unittest

from ..inmemory import (
    DataValueInMemory, DataStreamInMemory, DataStoreNestableInMemory)


class TestDataValueInMemory(unittest.TestCase):

    def setUp(self):
        self.ds = DataValueInMemory()

    def test_set_get(self):
        obj = object()
        self.ds.set(obj)
        self.assertTrue(self.ds.get() is obj)


class TestDataStreamInMemory(unittest.TestCase):

    def setUp(self):
        self.ds = DataStreamInMemory()

    def test_write_read(self):
        data = 'some text'
        with self.ds.open() as f:
            f.write(data)
        self.assertTrue(self.ds.stream.closed)

        with self.ds.open() as f:
            written = f.read()
        self.assertEqual(written, data)


class TestDataStoreNestableInMemory(unittest.TestCase):

    def setUp(self):
        self.ds = DataStoreNestableInMemory()

    def test_one_value(self, ds=None):
        ds = ds or self.ds
        data = dict(a=1)
        key = 'key_value'
        ds[key] = data
        self.assertEqual(ds[key], data)

    def test_one_stream(self, ds=None):
        ds = ds or self.ds
        data = 'some text'
        key = 'key_stream'
        with ds.get_filestore(key).open() as s:
            s.write(data)

        with ds.get_filestore(key).open() as s:
            written = s.read()
        self.assertEqual(written, data)

    def test_nested_store(self):
        ds = self.ds
        key = 'key_nested'
        subds = ds.get_substore(key)
        self.test_one_value(subds)
        self.test_one_stream(subds)
        self.assertTrue(ds[key] is subds)
