import json

from .base import BaseKVStore


class KVStoreJSON(BaseKVStore):

    def load(self, fp):
        self._db = json.load(fp)

    def dump(self, fp):
        json.dump(self._db, fp)

    @staticmethod
    def _filtered_key(key):
        # convert tuples to list, etc.
        # there should be lot better way to do this...
        return json.loads(json.dumps(key))
