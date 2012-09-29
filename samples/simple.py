import os

from buildlet.datastore import DataAutoDirectoryWithMagic
from buildlet.task import BaseCachedTask, BaseSimpleTask
from buildlet.runner import getrunner, listrunner


class BaseSimpleCachedTask(BaseSimpleTask, BaseCachedTask):

    def run(self):
        print "Running {0}...".format(self)


class SimpleRootTask(BaseSimpleCachedTask):

    num_parents = 3

    def __init__(self, basepath, **kwds):
        # Use absolute path for IPython runner
        basepath = os.path.abspath(basepath)
        self.datastore = DataAutoDirectoryWithMagic(basepath)
        super(SimpleRootTask, self).__init__(basepath=basepath, **kwds)
        if self.clean:
            self.datastore.clean()

    def generate_parents(self):
        return [
            BaseSimpleCachedTask(
                # Only string key is supported by all nestable
                # data store types.
                datastore=self.datastore.get_substore(str(i)))
            for i in range(self.num_parents)]


def run_simple_task(runner_class, **kwds):
    task = SimpleRootTask(**kwds)
    runner = getrunner(runner_class)()
    print "Runner:", runner
    runner.run(task)


def main(args=None):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--basepath', default="tmp")
    parser.add_argument('--num-parents', type=int,
                        default=SimpleRootTask.num_parents)
    parser.add_argument('--runner-class', choices=sorted(listrunner()),
                        default='SimpleRunner')
    parser.add_argument('--clean', default=False, action='store_true')
    ns = parser.parse_args(args)
    run_simple_task(**vars(ns))


if __name__ == '__main__':
    main()
