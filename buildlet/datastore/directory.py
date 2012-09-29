"""
File system directory oriented data store.
"""

import os
import shutil

from .base import (
    BaseDataDirectory, BaseDataStream, MixInDataStoreFileSystem,
    MixInDataStoreNestableMetaInKey, METAKEY)

from .autoserialize import BaseDataValueAutoSerialize, DataValuePickle


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


class _DataDirectory(BaseDataDirectory):

    """
    **Unsafe** internal implementation of :class:`DataDirectory`.

    This class is unsafe to use as-is because there is no mechanism
    to make sure key is different from :attr:`metakey`.  Child class
    must either use :class:`MixInDataStoreNestableMetaInKey` or
    override :meth:`aspath`.

    """

    default_streamstore_type = DataFile
    default_valuestore_type = DataValuePickle

    metakey = METAKEY
    # this is needed to use this class w/o MixInDataStoreNestableMetaInKey.

    def __init__(self, *args, **kwds):
        super(_DataDirectory, self).__init__(*args, **kwds)
        mkdirp(self.path)

    def get_metastorepath(self):
        return os.path.join(self.path, self.metakey)

    @property
    def default_metastore_kwds(self):
        return dict(path=self.get_metastorepath())

    def aspath(self, key):
        return os.path.join(self.path, key)

    def __iter__(self):
        return iter(os.listdir(self.path))

    def __delitem__(self, key):
        path = self.aspath(key)
        if not os.path.exists(path):
            raise KeyError(
                'Key {0} (path: {1}) does not exist'.format(key, path))
        if os.path.isdir(path):
            shutil.rmtree(self.aspath(key))
        else:
            os.remove(path)

    def __getitem__(self, key):
        path = self.aspath(key)
        if not os.path.exists(path):
            raise KeyError(key)
        if os.path.isdir(path):
            cls = self.default_substore_type
            return cls(path=path)
        else:
            return self.default_streamstore_type(path=path)

    def __setitem__(self, key, value):
        path = self.aspath(key)
        if isinstance(value, BaseDataDirectory):
            mkdirp(path)
        elif isinstance(value, (DataFile, BaseDataValueAutoSerialize)):
            if not os.path.exists(path):
                open(path, 'wb').close()
        else:
            raise ValueError(
                'Value {0!r} is not supported data store type.'.format(value))


class DataDirectory(MixInDataStoreNestableMetaInKey, _DataDirectory):
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
