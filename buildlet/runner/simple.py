def run(task):
    task.pre_run()
    try:
        if task.is_finished():
            task.load()
        else:
            for parent in task.get_parents():
                run(parent)
            task.run()
    finally:
        task.post_run()
