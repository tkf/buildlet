import unittest
import tempfile
import shutil

from ..directory import DataFile, DataDirectory
from .mixintestcase import MixInStreamTestCase, MixInNestableTestCase


class TestDataFile(MixInStreamTestCase, unittest.TestCase):

    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile()
        self.ds = DataFile(self.tempfile.name)

    def tearDown(self):
        self.tempfile.close()


class TestDataDirectory(MixInNestableTestCase, unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.ds = DataDirectory(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
