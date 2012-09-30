from buildlet.task import BaseSimpleCachedTask
from buildlet.runner import run, listrunner


class SimpleCachedTask(BaseSimpleCachedTask):

    def run(self):
        self.datastore['result'] = {'key': 1}
        print "Running {0}...".format(self)


class SimpleCachedRootTask(SimpleCachedTask):

    num_parents = 3

    def __init__(self, **kwds):
        super(SimpleCachedRootTask, self).__init__(**kwds)

        # --clear-before-run
        for i in range(self.num_parents):
            self.datastore.get_substore(str(i))
            # so that `self.datastore.clear` clears substore.
        if self.clear_before_run:
            self.datastore.clear()

    def generate_parents(self):
        return [
            SimpleCachedTask(
                # Only string key is supported by all nestable
                # data store types.
                datastore=self.datastore.get_substore(str(i)))
            for i in range(self.num_parents)]


def run_simple_task(runner_class, **kwds):
    task = SimpleCachedRootTask(**kwds)
    print "Runner:", runner_class
    runner = run(runner_class, task)
    return (runner, task)


def main(args=None):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--basepath', default="tmp")
    parser.add_argument('--num-parents', type=int,
                        default=SimpleCachedRootTask.num_parents)
    parser.add_argument('--runner-class', choices=sorted(listrunner()),
                        default='SimpleRunner')
    parser.add_argument('--clear-before-run', '-c', default=False,
                        action='store_true')
    ns = parser.parse_args(args)
    return run_simple_task(**vars(ns))


if __name__ == '__main__':
    ret = main()
