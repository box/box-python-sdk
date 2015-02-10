# coding: utf-8

from __future__ import unicode_literals
import pytest
from boxsdk.util.lru_cache import LRUCache


@pytest.fixture
def lru_cache():
    return LRUCache()


@pytest.fixture
def keys():
    return ['key1', 'key2', 'key3']


def test_lru_cache_returns_minus_one_for_missing_key(lru_cache, keys):
    # pylint:disable=redefined-outer-name
    for key in keys:
        with pytest.raises(KeyError):
            lru_cache.get(key)


def test_lru_cache_returns_none_for_existing_key(lru_cache, keys):
    # pylint:disable=redefined-outer-name
    for key in keys:
        lru_cache.set(key)
        assert lru_cache.get(key) is None


def test_lru_cache_ejects_least_recently_used_key(lru_cache, keys):
    # pylint:disable=redefined-outer-name
    lru_cache.capacity = len(keys)
    for key in keys:
        lru_cache.set(key)
    lru_cache.set('another key')
    with pytest.raises(KeyError):
        lru_cache.get(keys[0])
    assert lru_cache.get('another key') is None
    for key in keys[1:]:
        assert lru_cache.get(key) is None
    lru_cache.set('yet another key')
    with pytest.raises(KeyError):
        lru_cache.get('another key')
