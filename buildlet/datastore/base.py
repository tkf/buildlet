"""
Base data store classes.
"""

import collections
import itertools

from ..utils.hashutils import hexdigest

METAKEY = '.buildlet'


class BaseDataStore(object):

    def clear(self):
        raise NotImplementedError

    def hash(self):
        """
        Return some comparable object for automatic dependency check.

        To enable automatic dependency check, child class must define
        this function.  Returning `None` (default) means to always
        re-run tasks.

        """
        return None


class BaseDataValue(BaseDataStore):

    def set(self, value):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class BaseDataStream(BaseDataStore):

    path = None

    def exists(self):
        raise NotImplementedError

    def open(self, *args):
        raise NotImplementedError


class BaseDataStoreNestable(collections.MutableMapping, BaseDataStore):

    """
    Base class for nestable data store.
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

    default_metastore_type = None
    """
    Default class for metadata store.
    None means same as :attr:`default_substore_type` or this class.
    """

    default_metastore_kwds = None
    """
    Default keyword arguments to given to :attr:`default_metastore_type`.
    None means no argument.
    """

    def get_substore_type(self):
        return self.default_substore_type or self.__class__

    def get_metastore_type(self):
        return self.default_metastore_type or self.get_substore_type()

    def get_substore(self, key, dstype=None, dskwds={},
                     allow_specialkeys=False):
        """
        Get or create sub-data store under `key`.

        If requested data store does not exist, it is initialized
        by ``dstype(**dskwds)``.  If `dstype` is None,
        :attr:`default_substore_type` is used instead.

        """
        if dstype is None:
            dstype = self.get_substore_type()
        if key in self:
            s = self[key]
            if not isinstance(s, dstype):
                raise ValueError(
                    "Cannot create sub-data store for key '{0}'.\n"
                    "Data store of type {1} is requested, but "
                    "current value {2!r} is not instance of it."
                    .format(key, dstype, s))
            return s
        s = dstype(**dskwds)
        self.__setitem__(key, s)
        return s

    def get_filestore(self, key, dstype=None, dskwds={}):
        """
        Get or create stream type data store under `key`.

        Default `dstype` is defined by :attr:`default_streamstore_type`.
        See also :meth:`get_substore`.

        """
        if dstype is None:
            dstype = self.default_streamstore_type
        return self.get_substore(key, dstype, dskwds)

    def get_valuestore(self, key, dstype=None, dskwds={}):
        """
        Get or create value type data store under `key`.

        Default `dstype` is defined by :attr:`default_valuestore_type`.
        See also :meth:`get_substore`.

        """
        if dstype is None:
            dstype = self.default_valuestore_type
        return self.get_substore(key, dstype, dskwds)

    _metastore = None

    def get_metastore(self):
        if self._metastore:
            return self._metastore
        dstype = self.get_metastore_type()
        dskwds = self.default_metastore_kwds or {}
        self._metastore = dstype(**dskwds)
        return self._metastore

    def __len__(self):
        """
        Safe and stupid `len` implementation based on :meth:`__iter__`

        Child class author can override this function, but must be
        careful about :meth:`specialkeys`.

        """
        return sum(1 for _ in self)

    def hash(self):
        strings = []
        for key in itertools.chain(sorted(self)):
            store = self[key]
            subhash = store.hash()
            if subhash is None:
                return None
            strings.append(key)
            strings.append(subhash)
        strings.apppend(self.__class__.__name__)
        return hexdigest(strings)


class MixInDataStoreNestableMetaInKey(BaseDataStoreNestable):

    """
    Mix-in class for datastore

    Use this class for datastores in which metastore shares namespace.
    For example, when the key is a file name in a directory and
    metastore must be in the same directory, you need to protect
    a key for metadata.

    """

    metakey = METAKEY
    """
    Key to store metadata.
    """

    specialkeys = (metakey,)
    """
    Special purpose keys.  Trying to set this key raise an error.
    """

    def __assert_not_specialkeys(self, key):
        if key in self.specialkeys:
            raise KeyError('{0} is a special key'.format(key))

    def get_substore(self, key, dstype=None, dskwds={},
                     _allow_specialkeys=False, **kwds):
        if not _allow_specialkeys:
            self.__assert_not_specialkeys(key)
        return super(MixInDataStoreNestableMetaInKey, self) \
            .get_substore(key, dstype=dstype, dskwds=dskwds, **kwds)

    def __setitem__(self, key, value):
        self.__assert_not_specialkeys(key)
        super(MixInDataStoreNestableMetaInKey, self).__setitem__(key, value)

    def __delitem__(self, key):
        self.__assert_not_specialkeys(key)
        super(MixInDataStoreNestableMetaInKey, self).__delitem__(key)

    def __iter__(self):
        return itertools.ifilterfalse(
            lambda k: k in self.specialkeys,
            super(MixInDataStoreNestableMetaInKey, self).__iter__())


class MixInDataStoreNestableAutoValue(BaseDataStoreNestable):

    """
    Mix-in class for fancy automatic get/set.

    Storing Python object is simply done by::

      ds[key] = value

    To load value, simply do::

      value = ds[key]

    Here, `value` must be serialise-able by the data store
    specified by :attr:`default_valuestore_type`.

    """

    def __getitem__(self, key):
        value = super(MixInDataStoreNestableAutoValue, self).__getitem__(key)
        if isinstance(value, BaseDataValue):
            return value.get()
        else:
            return value

    def __setitem__(self, key, value):
        if isinstance(value, BaseDataStore):
            super(MixInDataStoreNestableAutoValue, self) \
                .__setitem__(key, value)
        else:
            store = self.get_valuestore(key)
            store.set(value)


class MixInDataStoreFileSystem(BaseDataStore):

    def __init__(self, path, *args, **kwds):
        self.path = path
        super(MixInDataStoreFileSystem, self).__init__(*args, **kwds)

    def aspath(self, key):
        raise NotImplementedError


class BaseDataDirectory(MixInDataStoreFileSystem, BaseDataStoreNestable):

    def get_substore(self, key, dstype=None, dskwds={}, **kwds):
        if 'path' not in dskwds:
            dskwds = dskwds.copy()
            dskwds['path'] = self.aspath(key)
        return super(BaseDataDirectory, self) \
            .get_substore(key, dstype=dstype, dskwds=dskwds, **kwds)


# -------------------------------------------------------------------------
# Utility functions
# -------------------------------------------------------------------------


def is_datastore(obj):
    return isinstance(obj, BaseDataStore)


def assert_datastore(obj, exception=AssertionError):
    if not is_datastore(obj):
        raise exception("`{0!r}` is not datastore.".format(obj))
