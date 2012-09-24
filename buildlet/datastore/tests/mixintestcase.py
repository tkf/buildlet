class BaseMixnInTestCase(object):

    def setUp(self):
        raise NotImplementedError(
            'You must set data store `self.ds` here!')


class MixInValueTestCase(BaseMixnInTestCase):

    def test_set_get(self):
        data = dict(a=1)
        self.ds.set(data)
        self.assertEqual(self.ds.get(), data)


class MixInStreamTestCase(BaseMixnInTestCase):

    def test_write_read(self):
        data = 'some text'
        with self.ds.open() as f:
            f.write(data)
        self.assertTrue(self.ds.stream.closed)

        with self.ds.open() as f:
            written = f.read()
        self.assertEqual(written, data)


class MixInNestableTestCase(BaseMixnInTestCase):

    key_nested = 'key_nested'

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
        key = self.key_nested
        subds = ds.get_substore(key)
        self.assertTrue(ds[key] is subds)
        self.test_one_stream(subds)


class MixInNestableAutoValueTestCase(MixInNestableTestCase):

    def test_one_value(self, ds=None):
        ds = ds or self.ds
        data = dict(a=1)
        key = 'key_value'
        ds[key] = data
        self.assertEqual(ds[key], data)

    def test_nested_store(self):
        super(MixInNestableAutoValueTestCase, self).test_nested_store()
        self.test_one_value(self.ds[self.key_nested])
