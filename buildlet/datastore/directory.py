"""
File system directory oriented data store.
"""

import os
import shutil

from .base import BaseDataDirectory, BaseDataStream, MixInDataStoreFileSystem


def mkdirp(path):
    """Do ``mkdir -p {path}``"""
    if not os.path.isdir(path):
        os.makedirs(path)


class DataFile(MixInDataStoreFileSystem, BaseDataStream):

    def open(self, *args, **kwds):
        return open(self.path, *args, **kwds)


class DataDirectory(BaseDataDirectory):

    default_streamstore_type = DataFile

    def __init__(self, *args, **kwds):
        super(DataDirectory, self).__init__(*args, **kwds)
        mkdirp(self.path)

    def aspath(self, key):
        return os.path.join(self.path, key)

    def _listdir(self):
        return os.listdir(self.path)

    def __len__(self):
        return len(self._listdir)

    def __iter__(self):
        sep = os.path.sep
        for key in self._listdir():
            if os.path.isdir(self.aspath(key)) and not key.endswith(sep):
                yield key + sep
            else:
                yield key

    def _del_store(self, key):
        path = self.aspath(key)
        if not os.path.exists(path):
            raise KeyError(
                'Key {0} (path: {1}) does not exist'.format(key, path))
        if os.path.isdir(path):
            shutil.rmtree(self.aspath(key))
        else:
            os.remove(path)

    def _get_store(self, key):
        path = self.aspath(key)
        if key.endswith(os.path.sep):
            cls = self.default_substore_type or self.__class__
            return cls(path=path)
        else:
            return self.default_streamstore_type(path=path)

    def _set_store(self, key, value):
        path = self.aspath(key)
        if isinstance(value, BaseDataDirectory):
            mkdirp(path)
        elif isinstance(value, DataFile) and not os.path.exists(path):
            open(path, 'w').close()
        else:
            raise ValueError(
                'Value {0!r} is not supported data store type.'.format(value))
