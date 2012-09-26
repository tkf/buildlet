from ..utils import _pickle as pickle

from .base import BaseKVStore


class KVStorePickle(BaseKVStore):

    mode = 'b'

    def load(self, fp):
        self._db = pickle.load(fp)

    def dump(self, fp):
        pickle.dump(self._db, fp)
