import os
import collections


def mkdirp(path):
    """Do ``mkdir -p {path}``"""
    if not os.path.isdir(path):
        os.makedirs(path)


class memoizemethod(object):

    """
    Per-instance memoization of instance method.

    >>> class Example(object):
    ...
    ...     @memoizemethod
    ...     def f(self, a):
    ...         print('Called with: {0}'.format(a))
    ...         return a
    >>> eg = Example()
    >>> eg.f(1)
    Called with: 1
    1
    >>> eg.f(1)  # `Example.f` is not called here
    1
    >>> eg.f(2)  # Try with another argument
    Called with: 2
    2
    >>> eg.f(2)
    2
    >>> eg.f(1)
    1

    Method can take non-hashable object, but then you won't
    have caching.

    >>> eg.f({1: 2})
    Called with: {1: 2}
    {1: 2}
    >>> eg.f({1: 2})
    Called with: {1: 2}
    {1: 2}


    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, _=None):
        if instance is None:
            return self.func

        def memoizedmethod(*args, **kwds):
            return self(instance, *args, **kwds)

        return memoizedmethod

    def __call__(self, instance, *args, **kwds):
        try:
            cache = instance.__cache
        except AttributeError:
            cache = instance.__cache = {}

        try:
            kwds_set = frozenset(kwds.items())
            frozenset(args)  # check if `args` is hashable
        except TypeError:
            # Argument is not hashable.
            return self.func(instance, *args, **kwds)

        key = (self.func, args, kwds_set)
        if key in cache:
            return cache[key]
        res = cache[key] = self.func(instance, *args, **kwds)
        return res
