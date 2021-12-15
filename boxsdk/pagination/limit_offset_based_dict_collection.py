# coding: utf-8

from .dict_page import DictPage
from .limit_offset_based_object_collection import LimitOffsetBasedObjectCollection


class LimitOffsetBasedDictCollection(LimitOffsetBasedObjectCollection):
    """Represents a limit/offset-based collection of simple dicts, which are not translated into objects."""
    _page_constructor = DictPage
