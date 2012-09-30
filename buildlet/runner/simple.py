from .base import BaseRunner


class SimpleRunner(BaseRunner):

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
                # This is redundant because `.load` or `.run` is called
                # for *all* tasks regardless the state (need rerun or not).
                cls.run(parent)
            if task.is_finished():
                task.load()
            else:
                task.run()
            task.post_success_run()
        except Exception as e:
            task.post_error_run(e)
            raise
