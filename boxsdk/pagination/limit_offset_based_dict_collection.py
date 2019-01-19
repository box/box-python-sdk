# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .dict_page import DictPage
from .limit_offset_based_object_collection import LimitOffsetBasedObjectCollection


class LimitOffsetBasedDictCollection(LimitOffsetBasedObjectCollection):
    """Represents a limit/offset-based collection of simple dicts, which are not translated into objects."""
    _page_constructor = DictPage
