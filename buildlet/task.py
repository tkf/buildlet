class TaskBase(object):

    def get_parents(self):
        return []

    def do_run(self):
        pass

    def load(self):
        pass

    def run(self):
        pass

    def pre_run(self):
        pass

    def post_run(self):
        pass

    def is_finished(self):
        return False


class SimpleTaskBase(TaskBase):

    _parents = None

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def generate_parents(self):
        return []

    def get_parents(self):
        if self._parents is None:
            self._parents = self.generate_parents()
        return self._parents
