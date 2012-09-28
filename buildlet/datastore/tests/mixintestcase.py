import os
import tempfile
import shutil


class BaseMixnInTestCase(object):

    @property
    def dstype(self):
        raise NotImplementedError(
            "Child class must set `dstype` to a data store class.")

    def setUp(self):
        self.ds = self.dstype()

    def set_some_value(self):
        raise NotImplementedError

    def test_hash(self):
        self.set_some_value()
        val = self.ds.hash()
        if val is None or isinstance(val, (basestring, int)):
            return
        assert hasattr(val, '__eq__'), \
            "`{0!r}` does not have __eq__".format(val)


class MixInValueTestCase(BaseMixnInTestCase):

    def test_set_get(self):
        data = dict(a=1)
        self.ds.set(data)
        self.assertEqual(self.ds.get(), data)

    def set_some_value(self):
        self.test_set_get()


class MixInStreamTestCase(BaseMixnInTestCase):

    def test_write_read(self):
        data = 'some text'.encode()
        with self.ds.open('w+b') as f:
            f.write(data)
        self.assertTrue(self.ds.stream.closed)

        with self.ds.open('rb') as f:
            written = f.read()
        self.assertEqual(written, data)

    def test_clear_and_exists(self):
        assert not self.ds.exists()
        self.test_write_read()
        assert self.ds.exists()
        self.ds.clear()
        assert not self.ds.exists()

    def set_some_value(self):
        self.test_write_read()


class MixInNestableTestCase(BaseMixnInTestCase):

    key_nested = 'key_nested'

    def test_one_stream(self, ds=None):
        ds = ds or self.ds
        data = 'some text'.encode()
        key = 'key_stream'
        with ds.get_filestore(key).open('w+b') as s:
            s.write(data)

        with ds.get_filestore(key).open('rb') as s:
            written = s.read()
        self.assertEqual(written, data)

    def test_nested_store(self):
        ds = self.ds
        key = self.key_nested
        subds = ds.get_substore(key)
        self.assertEqual(ds[key], subds)
        self.test_one_stream(subds)

    def check_clear(self, ds, adder):
        self.assertEqual(sorted(ds), [])

        keys = sorted(['a', 'b', 'c'])
        for key in keys:
            adder(key)

        self.assertEqual(sorted(ds), keys)
        self.ds.clear()
        self.assertEqual(sorted(ds), [])

    def test_clear_filestore(self):
        ds = self.ds

        def add_filestore(key):
            with ds.get_filestore(key).open('w+b') as s:
                s.write('dummy'.encode())

        self.check_clear(ds, add_filestore)

    def test_clear_substore(self):
        ds = self.ds
        self.check_clear(ds, ds.get_substore)

    def test_metastore(self):
        ms = self.ds.get_metastore()
        assert isinstance(ms, self.ds.default_metastore_type)

    def set_some_value(self):
        self.test_nested_store()


class MixInNestableAutoValueTestCase(MixInNestableTestCase):

    def test_one_value(self, ds=None):
        ds = ds or self.ds
        data = dict(a=1)
        key = 'key_value'
        ds[key] = data
        self.assertEqual(ds[key], data)

        new_data = range(3)
        ds_value = ds.get_valuestore(key)
        self.assertEqual(ds_value.get(), data)
        ds_value.set(new_data)
        self.assertEqual(ds[key], new_data)

    def test_one_value_reverse(self, ds=None):
        ds = ds or self.ds
        data = dict(a=1)
        key = 'key_value'
        ds_value = ds.get_valuestore(key)
        ds_value.set(data)
        self.assertEqual(ds_value.get(), data)

        new_data = range(3)
        self.assertEqual(ds[key], data)
        ds[key] = new_data
        self.assertEqual(ds_value.get(), new_data)

    def test_nested_store(self):
        super(MixInNestableAutoValueTestCase, self).test_nested_store()
        self.test_one_value(self.ds[self.key_nested])


class MixInWithTempDirectory(BaseMixnInTestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.ds = self.dstype(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)


class MixInWithTempFile(MixInWithTempDirectory):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.tempfilename = os.path.join(self.tempdir, 'tempfile')
        self.ds = self.dstype(self.tempfilename)
