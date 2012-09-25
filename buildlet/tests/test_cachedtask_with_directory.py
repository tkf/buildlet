import tempfile
import shutil

from ..datastore.directory import DataDirectory

from .test_cachedtask import TestCachedTask


class TestCachedTaskWithDirectory(TestCachedTask):

    DataStoreClass = DataDirectory

    def setup_datastore(self):
        self.tempdir = tempfile.mkdtemp()
        self.ds = self.DataStoreClass(self.tempdir)

    def teardown_datastore(self):
        shutil.rmtree(self.tempdir)
