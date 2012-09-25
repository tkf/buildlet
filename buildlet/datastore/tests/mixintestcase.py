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


class MixInValueTestCase(BaseMixnInTestCase):

    def test_set_get(self):
        data = dict(a=1)
        self.ds.set(data)
        self.assertEqual(self.ds.get(), data)


class MixInStreamTestCase(BaseMixnInTestCase):

    def test_write_read(self):
        data = 'some text'
        with self.ds.open('w+b') as f:
            f.write(data)
        self.assertTrue(self.ds.stream.closed)

        with self.ds.open() as f:
            written = f.read()
        self.assertEqual(written, data)

    def test_clear_and_exists(self):
        assert not self.ds.exists()
        self.test_write_read()
        assert self.ds.exists()
        self.ds.clear()
        assert not self.ds.exists()


class MixInNestableTestCase(BaseMixnInTestCase):

    key_nested = 'key_nested'

    def test_one_stream(self, ds=None):
        ds = ds or self.ds
        data = 'some text'
        key = 'key_stream'
        with ds.get_filestore(key).open('w+b') as s:
            s.write(data)

        with ds.get_filestore(key).open() as s:
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
                s.write('dummy')

        self.check_clear(ds, add_filestore)

    def test_clear_substore(self):
        ds = self.ds
        self.check_clear(ds, ds.get_substore)

    def test_metastore(self):
        ms = self.ds.get_metastore()
        assert isinstance(ms, ms.__class__)


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


class MixInWithTempFile(BaseMixnInTestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.tempfile = tempfile.NamedTemporaryFile()
        self.ds = self.dstype(self.tempfile.name)

    def tearDown(self):
        self.tempfile.close()


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
