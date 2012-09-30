from ..utils import _pickle as pickle

from .base import BaseKVStore


class KVStorePickle(BaseKVStore):

    """
    Pickle based key-value store.

    >>> import os
    >>> from buildlet.utils.tempdir import TemporaryDirectory
    >>> with TemporaryDirectory() as tempdir:
    ...     kvs = KVStorePickle(os.path.join(tempdir, 'kvstore'))
    ...     with kvs.autosync():
    ...         kvs[{'key': 'can be dictionary'}] = 'value'
    ...     with kvs.autosync():
    ...         print(kvs[{'key': 'can be dictionary'}])
    value

    """

    mode = 'b'

    def load(self, fp):
        self._db = pickle.load(fp)

    def dump(self, fp):
        pickle.dump(self._db, fp)
