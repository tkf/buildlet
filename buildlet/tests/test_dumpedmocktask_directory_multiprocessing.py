from ..runner.multiprocessingpool import MultiprocessingRunner

from . import test_dumpedmocktask_directory


class TestingMultiprocessingRunner(MultiprocessingRunner):

    def wait_tasks(self):
        super(TestingMultiprocessingRunner, self).wait_tasks()
        for task in self.nodetaskmap.values():
            task.load_mock()


class TestDumpedMockTaskDirectoryMultiprocessing(
        test_dumpedmocktask_directory.TestDumpedMockTaskDirectory):
    RunnerClass = TestingMultiprocessingRunner
