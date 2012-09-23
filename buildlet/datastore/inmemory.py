"""
In-memory data store, mainly for testing purpose.
"""

from .base import DataStoreBase


class InMemoryDataStore(DataStoreBase):

    def __init__(self):
        self.__data = {}

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]
