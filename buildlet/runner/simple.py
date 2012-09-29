class SimpleRunner(object):

    """
    Simple blocking task runner.
    """

    def run(self, task):
        """
        Simple blocking task runner.

        Run `task` and its unfinished ancestors.

        """
        primitive_run(task, self.do_run)

    def do_run(self, task):
        for parent in task.get_parents():
            self.run(parent)
        task.run()


def primitive_run(task, do_run):
    task.pre_run()
    try:
        if task.is_finished():
            task.load()
        else:
            do_run(task)
        task.post_success_run()
    except Exception as e:
        task.post_error_run(e)
        raise
