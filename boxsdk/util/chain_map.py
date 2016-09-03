# coding: utf-8

from __future__ import absolute_import, unicode_literals

from functools import wraps


__all__ = list(map(str, ['ChainMap']))


# pylint:disable=unused-import
try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap as _ChainMap

    # Make sure that `ChainMap` is a new-style class.
    @wraps(_ChainMap, updated=())
    class ChainMap(_ChainMap, object):
        __slots__ = ()
