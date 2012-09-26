"""
Data store on file system with automatically generated directory/file name.
"""

import os

from ..kvstore.jsonstore import KVStoreJSON
from .directory import DataDirectory


class DataAutoDirectory(DataDirectory):

    """
    Nestable data store on file system with automatic name assignment.

    How to use file-type data store under :class:`DataAutoDirectory`:

    >>> from buildlet.utils.tempdir import TemporaryDirectory
    >>> with TemporaryDirectory() as tempdir:
    ...     ds = DataAutoDirectory(tempdir)
    ...     # Any serialize-able complex key type can be used:
    ...     ds_stream = ds.get_filestore(('complex', 'key', 100))
    ...     with ds_stream.open('w') as f:
    ...         f.write('some data')
    ...     with ds_stream.open() as f:
    ...         print f.read()
    some data


    How to make nested data store:

    >>> with TemporaryDirectory() as tempdir:
    ...     ds = DataAutoDirectory(tempdir)
    ...     ds_nested = ds.get_substore(('very', 'complex', 'key'))
    ...     print ds_nested                            # doctest: +ELLIPSIS
    <buildlet.datastore.autodirectory.DataAutoDirectory object at ...>

    """

    KeyPathMapClass = KVStoreJSON
    default_metastore_type = DataDirectory
    _pathwidth = 3

    def __init__(self, *args, **kwds):
        super(DataAutoDirectory, self).__init__(*args, **kwds)
        self.get_metastore()
        self.keypathmap = self.KeyPathMapClass(self.get_keypathmappath())

    def get_metastorepath(self):
        return os.path.join(self.path, self.metakey)

    def get_metastore(self):
        return self.default_metastore_type(self.get_metastorepath())

    def get_keypathmappath(self):
        return os.path.join(self.get_metastorepath(), 'keypathmap')

    def newpath(self, db):
        values = db.values()
        if values:
            next = max((int(v, 16) for v in values)) + 1
        else:
            next = 0
        path = '{0:0{1}x}'.format(next, self._pathwidth)
        assert path != self.metakey
        return path

    def getpath(self, key):
        db = self.keypathmap
        if key in db:
            path = db[key]
        else:
            db[key] = path = self.newpath(db)
        return path

    def aspath(self, key):
        subpath = self.getpath(key)
        return os.path.join(self.path, subpath)

    def __len__(self):
        return len(self.keypathmap)

    def __iter__(self):
        return iter(self.keypathmap)

    def _del_store(self, key):
        with self.keypathmap.autosync():
            super(DataAutoDirectory, self)._del_store(key)
            del self.keypathmap[key]

    def _get_store(self, key):
        with self.keypathmap.autosync():
            return super(DataAutoDirectory, self)._get_store(key)

    def _set_store(self, key, value):
        with self.keypathmap.autosync():
            self.getpath(key)
            super(DataAutoDirectory, self)._set_store(key, value)
