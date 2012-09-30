class SimpleRunner(object):

    """
    Simple blocking task runner.
    """

    @classmethod
    def run(cls, task):
        """
        Simple blocking task runner.

        Run `task` and its unfinished ancestors.

        """
        task.pre_run()
        try:
            for parent in task.get_parents():
                cls.run(parent)
            if task.is_finished():
                task.load()
            else:
                task.run()
            task.post_success_run()
        except Exception as e:
            task.post_error_run(e)
            raise
