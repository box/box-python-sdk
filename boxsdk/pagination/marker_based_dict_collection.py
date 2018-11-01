# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .dict_page import DictPage
from .marker_based_object_collection import MarkerBasedObjectCollection


class MarkerBasedDictCollection(MarkerBasedObjectCollection):
    """Represents a marker-based collection of simple dicts, which are not translated into objects."""
    _page_constructor = DictPage
