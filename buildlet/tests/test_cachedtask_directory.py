import tempfile
import shutil

from ..datastore.directory import DataDirectory

# Avoid importing test case at top-level to duplicated test
from . import test_cachedtask


class MixInTestDataDirectory(object):

    DataStoreClass = DataDirectory

    def setup_datastore(self):
        self.tempdir = tempfile.mkdtemp()
        self.ds = self.DataStoreClass(self.tempdir)

    def teardown_datastore(self):
        shutil.rmtree(self.tempdir)


class TestCachedTaskDirectory(MixInTestDataDirectory,
                              test_cachedtask.TestCachedTask):
    pass
