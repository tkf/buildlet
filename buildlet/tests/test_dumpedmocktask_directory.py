from . import test_dumpedmocktask
from .test_cachedtask_directory import MixInTestDataDirectory


class TestDumpedMockTaskDirectory(MixInTestDataDirectory,
                                  test_dumpedmocktask.TestDumpedMockTask):
    pass
