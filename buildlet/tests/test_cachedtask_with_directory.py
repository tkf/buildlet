import tempfile
import shutil

from ..datastore.directory import DataDirectory

# Avoid importing test case at top-level to duplicated test
from . import test_cachedtask


class TestCachedTaskWithDirectory(test_cachedtask.TestCachedTask):

    DataStoreClass = DataDirectory

    def setup_datastore(self):
        self.tempdir = tempfile.mkdtemp()
        self.ds = self.DataStoreClass(self.tempdir)

    def teardown_datastore(self):
        shutil.rmtree(self.tempdir)
