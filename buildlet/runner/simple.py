class SimpleRunner(object):

    """
    Simple blocking task runner.
    """

    def run(self, task):
        """
        Simple blocking task runner.

        Run `task` and its unfinished ancestors.

        """
        primitive_run(task, self.run_parent)

    def run_parent(self, task):
        for parent in task.get_parents():
            self.run(parent)


def primitive_run(task, run_parent):
    task.pre_run()
    try:
        if task.is_finished():
            task.load()
        else:
            run_parent(task)
            task.run()
        task.post_success_run()
    except Exception as e:
        task.post_error_run(e)
        raise
