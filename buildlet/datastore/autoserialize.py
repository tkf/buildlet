from .base import MixInDataStoreFileSystem, BaseDataValue


class BaseDataValueAutoSerialize(MixInDataStoreFileSystem, BaseDataValue):

    def set(self, value):
        with open(self.path, 'w+b') as fp:
            self.dump(value, fp)

    def get(self):
        with open(self.path) as fp:
            return self.load(fp)

    def dump(self, obj, fp):
        raise NotImplementedError

    def load(self, fp):
        raise NotImplementedError


class DataValuePickle(BaseDataValueAutoSerialize):

    def dump(self, obj, fp):
        from ..utils import _pickle
        _pickle.dump(obj, fp)

    def load(self, fp):
        from ..utils import _pickle
        return _pickle.load(fp)


class DataValueJSON(BaseDataValueAutoSerialize):

    def dump(self, obj, fp):
        import json
        json.dump(obj, fp)

    def load(self, fp):
        import json
        return json.load(fp)


class DataValueYAML(BaseDataValueAutoSerialize):

    def dump(self, obj, fp):
        import yaml
        yaml.dump(obj, fp)

    def load(self, fp):
        import yaml
        return yaml.load(fp)
