from ..runner.multiprocessingpool import MultiprocessingRunner

from . import test_dumpedmocktask_directory


class TestDumpedMockTaskDirectoryMultiprocessing(
        test_dumpedmocktask_directory.TestDumpedMockTaskDirectory):
    RunnerClass = MultiprocessingRunner
