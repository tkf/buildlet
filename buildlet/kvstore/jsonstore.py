import json

from .base import BaseKVStore


class KVStoreJSON(BaseKVStore):

    """
    JSON based key-value store.

    >>> import os
    >>> from buildlet.utils.tempdir import TemporaryDirectory
    >>> with TemporaryDirectory() as tempdir:
    ...     kvs = KVStoreJSON(os.path.join(tempdir, 'kvstore'))
    ...     with kvs.autosync():
    ...         kvs[{'key': 'can be dictionary'}] = 'value'
    ...     with kvs.autosync():
    ...         print(kvs[{'key': 'can be dictionary'}])
    value

    Note that JSON can't distinguish tuple from list.
    Therefore, ``(0, 1, 2)`` and ``[0, 1, 2]`` means
    same key for this class.

    >>> with TemporaryDirectory() as tempdir:
    ...     kvs = KVStoreJSON(os.path.join(tempdir, 'kvstore'))
    ...     with kvs.autosync():
    ...         kvs[(0, 1, 2)] = 'another value'
    ...     with kvs.autosync():
    ...         print(kvs[[0, 1, 2]])   # Using list!
    another value

    """

    def load(self, fp):
        self._db = json.load(fp)

    def dump(self, fp):
        json.dump(self._db, fp)

    @staticmethod
    def filtered_key(key):
        # convert tuples to list, etc.
        # there should be lot better way to do this...
        return json.loads(json.dumps(key))
