"""
Simple mock with pickling support.
"""

import itertools


class Mock(object):

    def __init__(self):
        self.call_args_list = []
        self.side_effect = None

    def __call__(self, *args, **kwds):
        self.call_args_list.append((args, kwds))
        if isinstance(self.side_effect, Exception):
            raise self.side_effect

    @property
    def call_count(self):
        return len(self.call_args_list)

    def assert_called_once_with(self, *args, **kwds):
        assert self.call_count == 1, \
            "Expected to be called once. Called {0} times." \
            .format(self.call_count)
        assert self.call_args_list[0] == (args, kwds), \
            "Expected call: mock({0})\nActual call: mock({1})" \
            .format(formatcallarg(*self.call_args_list[0]),
                    formatcallarg(args, kwds))


def formatcallarg(args, kwds):
    fargs = map(repr, args)
    fkwds = ('='.join([k, repr(v)]) for (k, v) in kwds.iteritems())
    return ', '.join(itertools.chain(fargs, fkwds))
