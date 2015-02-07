# coding: utf-8

from __future__ import unicode_literals
from boxsdk.util.ordered_dict import OrderedDict


class LRUCache(object):
    def __init__(self, capacity=512):
        super(LRUCache, self).__init__()
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    def set(self, key, value=None):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value
