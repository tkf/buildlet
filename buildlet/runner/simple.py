class SimpleRunner(object):

    @classmethod
    def run(cls, task):
        """
        Simple blocking task runner.

        Run `task` and its unfinished ancestors.

        """
        task.pre_run()
        try:
            if task.is_finished():
                task.load()
            else:
                for parent in task.get_parents():
                    cls.run(parent)
                task.run()
            task.post_success_run()
        except Exception as e:
            task.post_error_run(e)
