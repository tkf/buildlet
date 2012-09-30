"""
Value store with automatic serialization (Pickle/JSON/YAML).
"""

import os

from .base import MixInDataStoreFileSystem, BaseDataValue


class BaseDataValueAutoSerialize(MixInDataStoreFileSystem, BaseDataValue):

    mode = 't'

    def set(self, value):
        with open(self.path, 'w' + self.mode) as fp:
            self.dump(value, fp)

    def get(self):
        with open(self.path, 'r' + self.mode) as fp:
            return self.load(fp)

    def clear(self):
        if self.exists():
            os.remove(self.path)

    def dump(self, obj, fp):
        raise NotImplementedError

    def load(self, fp):
        raise NotImplementedError


class DataValuePickle(BaseDataValueAutoSerialize):

    """
    Pickle-based value store.

    >>> from buildlet.utils.tempdir import TemporaryDirectory
    >>> with TemporaryDirectory() as tempdir:
    ...     ds = DataValuePickle(os.path.join(tempdir, 'tmp'))
    ...     ds.set({'some': 'data'})
    ...     ds.get()
    {'some': 'data'}

    """

    mode = 'b'

    def dump(self, obj, fp):
        from ..utils import _pickle
        _pickle.dump(obj, fp)

    def load(self, fp):
        from ..utils import _pickle
        return _pickle.load(fp)


class DataValueJSON(BaseDataValueAutoSerialize):

    """
    JSON-based value store.

    >>> from buildlet.utils.tempdir import TemporaryDirectory
    >>> with TemporaryDirectory() as tempdir:
    ...     ds = DataValueJSON(os.path.join(tempdir, 'tmp'))
    ...     ds.set({'some': 'data'})
    ...     print(ds.get()['some'])
    data

    """

    def dump(self, obj, fp):
        import json
        json.dump(obj, fp)

    def load(self, fp):
        import json
        return json.load(fp)


class DataValueYAML(BaseDataValueAutoSerialize):

    """
    YAML-based value store.

    >>> from buildlet.utils.tempdir import TemporaryDirectory
    >>> with TemporaryDirectory() as tempdir:
    ...     ds = DataValueYAML(os.path.join(tempdir, 'tmp'))
    ...     ds.set({'some': 'data'})
    ...     ds.get()
    {'some': 'data'}

    """

    def dump(self, obj, fp):
        import yaml
        yaml.dump(obj, fp)

    def load(self, fp):
        import yaml
        return yaml.load(fp)
