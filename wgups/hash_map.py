from collections import namedtuple
from typing import Callable

Item = namedtuple("Item", "key value")


class HashMap:
    def __init__(self, size: int = 10, default: Callable = None):
        self.size = size
        self._default = default
        # Initialize an empty hash map
        self._buckets = [list()] * size

    def set_default(self,default: Callable):
        self._default = default

    def _index(self, key):
        return hash(key) % self.size

    def _bucket(self, key):
        return self._buckets[self._index(key)]

    def __setitem__(self, key, value):
        new_item = Item(key, value)
        bucket = self._bucket(key)
        for item in bucket:
            if item.key == key:
                bucket.remove(item)
                bucket.append(new_item)
                break
        else:
            self._buckets[self._index(key)].append(new_item)

    def __getitem__(self, key):
        for item in self._bucket(key):
            if item.key == key:
                return item.value
        else:
            if self._default is not None:
                default_value = self._default()
                self.__setitem__(key, default_value)
                return default_value
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __delitem__(self, key):
        bucket = self._bucket(key)
        for item in bucket:
            if item.key == key:
                bucket.remove(item)
                break
        else:
            raise KeyError(key)

    def pop(self, key):
        value = self.__getitem__(key)
        self.__delitem__(key)
        return value

    def keys(self):
        all_keys = set()
        for bucket in self._buckets:
            bucket_keys = [item.key for item in bucket]
            all_keys.update(bucket_keys)
        return all_keys

    def __repr__(self):
        repr = "{"
        for key in self.keys():
            repr += f"'{key}': {self.__getitem__(key)}, "
        repr += "}"
        return repr
