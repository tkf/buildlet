import tempfile
import shutil

from ..datastore.directory import DataDirectory

from .test_cachedtask import TestCachedTask


class TestCachedTaskWithDirectory(TestCachedTask):

    DataStoreClass = DataDirectory

    def setup_task(self):
        self.tempdir = tempfile.mkdtemp()
        self.ds = self.DataStoreClass(self.tempdir)
        self.task = self.TaskClass(datastore=self.ds)

    def teardown_task(self):
        shutil.rmtree(self.tempdir)
