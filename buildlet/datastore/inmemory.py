"""
In-memory data store, mainly for testing purpose.
"""

import io
import collections

from .base import (
    assert_datastore, BaseDataValue, BaseDataStream, BaseDataStoreNestable,
    MixInDataStoreNestableAutoValue)


class DataValueInMemory(BaseDataValue):

    """
    In-memory value store.

    >>> ds = DataValueInMemory()
    >>> obj = object()
    >>> ds.set(obj)
    >>> ds.get() is obj
    True
    >>> ds.hash() == hash(obj)
    True

    """

    def clear(self):
        if hasattr(self, '_value'):
            del self._value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

    def exists(self):
        return hasattr(self, '_value')

    def hash(self):
        if isinstance(self._value, collections.Hashable):
            return hash(self._value)


class BytesIOWrapper(io.BytesIO):

    """
    Tweaked version of `io.BytesIO` which can do `getvalue` after close.

    >>> with BytesIOWrapper() as s:
    ...     _ = s.write('value'.encode())
    >>> print(s.getvalue().decode())
    value

    Note that you can't do this with `io.BytesIO` in stdlib.

    >>> with io.BytesIO() as s:
    ...     _ = s.write('value'.encode())
    >>> print(s.getvalue().decode())
    Traceback (most recent call last):
      ...
    ValueError: I/O operation on closed file.

    """

    __value = None

    def close(self):
        self.getvalue()
        super(BytesIOWrapper, self).close()

    def getvalue(self):
        if not self.closed:
            self.__value = super(BytesIOWrapper, self).getvalue()
        return self.__value


class DataStreamInMemory(BaseDataStream):

    """
    In-memory file-like data store.

    >>> ds = DataStreamInMemory()
    >>> with ds.open('wb') as f:
    ...     _ = f.write('some data'.encode())
    >>> with ds.open('rb') as f:
    ...     print(f.read().decode())
    some data

    """

    path = None
    stream = None

    def clear(self):
        self.stream = None

    def exists(self):
        return bool(self.stream)

    def open(self, *_):
        value = None
        if self.stream:
            value = self.stream.getvalue()
        self.stream = BytesIOWrapper(value)
        return self.stream

    def hash(self):
        if self.stream is None:
            return None
        value = self.stream.getvalue()
        if isinstance(value, collections.Hashable):
            return hash(value)


class DataStoreNestableInMemory(BaseDataStoreNestable):

    """
    Nestable in-memory data store

    >>> ds = DataStoreNestableInMemory()
    >>> ds_stream = ds.get_filestore('key_stream')
    >>> ds_stream                                      # doctest: +ELLIPSIS
    <buildlet.datastore.inmemory.DataStreamInMemory object at ...>

    Once data store is set, you can use ``ds[key]`` to get data store.

    >>> ds['key_stream'] is ds_stream
    True

    """

    default_streamstore_type = DataStreamInMemory
    default_valuestore_type = DataValueInMemory

    def __init__(self):
        self.__data = {}

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __delitem__(self, key):
        del self.__data[key]

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        assert_datastore(value, ValueError)
        self.__data[key] = value


class DataStoreNestableInMemoryAutoValue(MixInDataStoreNestableAutoValue,
                                         DataStoreNestableInMemory):
    """
    Nestable in-memory data store with "auto value" feature.

    You can also use ``ds[key]``-access to automatically set/get
    any Python object.

    >>> ds = DataStoreNestableInMemoryAutoValue()
    >>> ds['key'] = {'a': 1}
    >>> ds['key']
    {'a': 1}

    Internally, it is saved in a value store.  See:

    >>> ds_value = ds.get_valuestore('key')
    >>> ds_value.get()
    {'a': 1}
    >>> ds_value.set(range(3))
    >>> ds['key']
    [0, 1, 2]

    """
