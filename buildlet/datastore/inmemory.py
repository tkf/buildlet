"""
In-memory data store, mainly for testing purpose.
"""

import io
import collections

from .base import BaseDataStoreNestableAutoValue, BaseDataStream, BaseDataValue


class DataValueInMemory(BaseDataValue):

    def clear(self):
        if hasattr(self, '_value'):
            del self._value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

    def hash(self):
        if isinstance(self._value, collections.Hashable):
            return hash(self._value)


class BytesIOWrapper(io.BytesIO):

    """
    Tweaked version of `io.BytesIO` which can do `getvalue` after close.

    >>> with BytesIOWrapper() as s:
    ...     s.write('value')
    >>> s.getvalue()
    'value'

    Note that you can't do this with `io.BytesIO` in stdlib.

    >>> with io.BytesIO() as s:
    ...     s.write('value')
    >>> s.getvalue()
    Traceback (most recent call last)
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

    path = None
    stream = None

    def clear(self):
        self.stream = None

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


class DataStoreNestableInMemory(BaseDataStoreNestableAutoValue):

    default_streamstore_type = DataStreamInMemory
    default_valuestore_type = DataValueInMemory

    def __init__(self):
        self.__data = {}

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def _del_store(self, key):
        del self.__data[key]

    def _get_store(self, key):
        return self.__data[key]

    def _set_store(self, key, value):
        self.__data[key] = value
