import os
import collections
from contextlib import contextmanager
import json


class KVStoreJSON(collections.MutableMapping):

    def __init__(self, path):
        self.path = path
        self._db = []

    def load(self, fp):
        self._db = json.load(fp)

    def dump(self, fp):
        json.dump(self._db, fp)

    @staticmethod
    def _filtered_key(key):
        # convert tuples to list, etc.
        # there should be lot better way to do this...
        return json.loads(json.dumps(key))

    def __getitem__(self, key):
        key = self._filtered_key(key)
        for (k, v) in self._db:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        del self[key]
        key = self._filtered_key(key)
        self._db.append((key, value))

    def __delitem__(self, key):
        key = self._filtered_key(key)
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
        if os.path.exists(self.path):
            with open(self.path) as fp:
                self.load(fp)
        yield self
        with file(self.path, 'w') as fp:
            self.dump(fp)
