import os
import collections
from contextlib import contextmanager


class BaseKVStore(collections.MutableMapping):

    def __init__(self, path):
        self.path = path
        self._db = []

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
        if os.path.exists(self.path):
            with open(self.path) as fp:
                self.load(fp)
        yield
        with open(self.path, 'wb') as fp:
            self.dump(fp)
