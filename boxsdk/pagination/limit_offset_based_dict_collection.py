# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .dict_page import DictPage
from .limit_offset_based_object_collection import LimitOffsetBasedObjectCollection


class LimitOffsetBasedDictCollection(LimitOffsetBasedObjectCollection):
    _page_constructor = DictPage
