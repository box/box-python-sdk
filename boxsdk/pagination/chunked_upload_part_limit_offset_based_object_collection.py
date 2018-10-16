# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .chunked_upload_part_page import ChunkedUploadPartPage
from .limit_offset_based_object_collection import LimitOffsetBasedObjectCollection


class ChunkedUploadPartLimitOffsetBasedObjectCollection(LimitOffsetBasedObjectCollection):
    _page_constructor = ChunkedUploadPartPage
