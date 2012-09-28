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

    """
    File based stream data store.

    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile() as temp:
    ...     ds = DataFile(temp.name)
    ...     with ds.open('wt') as f:
    ...         _ = f.write('some data')
    ...     with ds.open() as f:
    ...         print(f.read())
    some data

    """

    def clear(self):
        self.stream = None
        os.remove(self.path)

    def exists(self):
        return os.path.exists(self.path)

    def open(self, *args, **kwds):
        self.stream = open(self.path, *args, **kwds)
        return self.stream


class DataDirectory(BaseDataDirectory):

    """
    Directory based nestable data store.

    How to use file-type data store under :class:`DataDirectory`:

    >>> from buildlet.utils.tempdir import TemporaryDirectory
    >>> with TemporaryDirectory() as tempdir:
    ...     ds = DataDirectory(tempdir)
    ...     ds_stream = ds.get_filestore('key')
    ...     with ds_stream.open('wt') as f:
    ...         _ = f.write('some data')
    ...     with ds_stream.open() as f:
    ...         print(f.read())
    some data


    How to make nested data store:

    >>> with TemporaryDirectory() as tempdir:
    ...     ds = DataDirectory(tempdir)
    ...     ds_nested = ds.get_substore('key')
    ...     print(ds_nested)                           # doctest: +ELLIPSIS
    <buildlet.datastore.directory.DataDirectory object at ...>

    """

    default_streamstore_type = DataFile

    def __init__(self, *args, **kwds):
        super(DataDirectory, self).__init__(*args, **kwds)
        mkdirp(self.path)

    def aspath(self, key):
        return os.path.join(self.path, key)

    def _listdir(self):
        return os.listdir(self.path)

    def __len__(self):
        return len(self._listdir())

    def __iter__(self):
        for key in self._listdir():
            if os.path.isdir(self.aspath(key)):
                yield key
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
        if not os.path.exists(path):
            raise KeyError(key)
        if os.path.isdir(path):
            cls = self.get_substore_type()
            return cls(path=path)
        else:
            return self.default_streamstore_type(path=path)

    def _set_store(self, key, value):
        path = self.aspath(key)
        if isinstance(value, BaseDataDirectory):
            mkdirp(path)
        elif isinstance(value, DataFile) and not os.path.exists(path):
            open(path, 'wb').close()
        else:
            raise ValueError(
                'Value {0!r} is not supported data store type.'.format(value))
