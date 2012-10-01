from . import test_dumpedmocktask
from .test_cacheabletask_directory import MixInTestDataDirectory


class TestDumpedMockTaskDirectory(MixInTestDataDirectory,
                                  test_dumpedmocktask.TestDumpedMockTask):
    pass
