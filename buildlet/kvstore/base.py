import os
import collections
from contextlib import contextmanager

from ..utils import mkdirp


class BaseKVStore(collections.MutableMapping):

    """
    Base class for key-value stores.

    This class is mainly for data store class
    :class:`buildlet.datastore.autodirectory.DataAutoDirectory`.
    It is used for storing key-to-path map.

    """

    mode = 't'

    def __init__(self, path):
        self.path = path
        self._db = []
        self._mkdirp()

    def _mkdirp(self):
        mkdirp(os.path.dirname(self.path))

    def load(self, fp):
        raise NotImplementedError

    def dump(self, fp):
        raise NotImplementedError

    @staticmethod
    def filter_key(key):
        """
        Filter out some unserializeable details from `key`.
        """
        return key

    def __getitem__(self, key):
        key = self.filter_key(key)
        for (k, v) in self._db:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        del self[key]
        key = self.filter_key(key)
        self._db.append((key, value))

    def __delitem__(self, key):
        key = self.filter_key(key)
        self._db = [(k, v) for (k, v) in self._db if not k == key]

    def values(self):
        return [v for (k, v) in self._db]

    def __len__(self):
        return len(self._db)

    def __iter__(self):
        for (k, v) in self._db:
            yield k

    @contextmanager
    def autosync(self):
        """
        Context manger to automatically load/dump any change.
        """
        self._mkdirp()
        if os.path.exists(self.path):
            with open(self.path, 'r' + self.mode) as fp:
                self.load(fp)
        yield
        with open(self.path, 'w' + self.mode) as fp:
            self.dump(fp)
