"""
Base data store classes.
"""

import collections
import itertools

from ..hashutils import hexdigest


class BaseDataStore(object):

    def clear(self):
        raise NotImplementedError

    def hash(self):
        return None


class BaseDataValue(BaseDataStore):

    def set(self, value):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class BaseDataStream(BaseDataStore):

    path = None

    def open(self, *args):
        raise NotImplementedError


class BaseDataStoreNestable(collections.MutableMapping, BaseDataStore):

    metakey = '.buildlet'
    """
    Key to store metadata.
    """

    specialkeys = (metakey,)
    """
    Special purpose keys.  Trying to set this key raise an error.
    """

    default_substore_type = None
    """
    Default class for sub-data store.  None means same as this class.
    """

    default_streamstore_type = None
    """
    Default class for stream type data store.  Child class **must** define it.
    """

    default_valuestore_type = None
    """
    Default class for value type data store.  Child class **must** define it.
    """

    def _get_store(self, key):
        raise NotImplementedError

    def _set_store(self, key, value):
        raise NotImplementedError

    def _del_store(self, key):
        raise NotImplementedError

    def get_substore(self, key, dstype=None, dskwds={}):
        if dstype is None:
            dstype = self.default_substore_type or self.__class__
        if key in self:
            s = self[key]
            if not isinstance(s, dstype):
                raise ValueError(
                    'Data store of type {0} is requested, but '
                    'current value {1!r} is not instance of it.'
                    .format(dstype, s))
            return s
        s = dstype(**dskwds)
        self[key] = s
        return s

    def get_filestore(self, key, dstype=None, dskwds={}):
        if dstype is None:
            dstype = self.default_streamstore_type
        return self.get_substore(key, dstype, dskwds)

    def get_valuestore(self, key, dstype=None, dskwds={}):
        if dstype is None:
            dstype = self.default_valuestore_type
        return self.get_substore(key, dstype, dskwds)

    def get_metastore(self):
        return self.get_substore(self.metakey)

    def __getitem__(self, key):
        value = self._get_store(key)
        if isinstance(value, BaseDataValue):
            return value.get()
        else:
            return value

    def __setitem__(self, key, value):
        if key in self.specialkeys:
            raise KeyError('{0} is a special key'.format(key))
        if isinstance(value, BaseDataStore):
            self._set_store(key, value)
        else:
            store = self.get_valuestore(key)
            store.set(value)

    def __delitem__(self, key):
        if key in self.specialkeys:
            raise KeyError('{0} is a special key'.format(key))
        self._del_store(key)

    def hash(self):
        strings = []
        specialkeys = (k for k in self.specialkeys if k in self)
        for key in itertools.chain(sorted(self), specialkeys):
            store = self[key]
            subhash = store.hash()
            if subhash is None:
                return None
            strings.append(key)
            strings.append(subhash)
        strings.apppend(self.__class__.__name__)
        return hexdigest(strings)


class MixInDataStoreFileSystem(BaseDataStore):

    def __init__(self, path, *args, **kwds):
        self.path = path
        super(MixInDataStoreFileSystem, self).__init__(*args, **kwds)

    def aspath(self, key):
        raise NotImplementedError


class BaseDataDirectory(MixInDataStoreFileSystem, BaseDataStoreNestable):

    def get_substore(self, key, dstype=None, dskwds={}):
        if 'path' not in dskwds:
            dskwds = dskwds.copy()
            dskwds['path'] = self.aspath(key)
        super(BaseDataDirectory, self) \
            .get_file(key, dstype=dstype, dskwds=dskwds)
