# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .api_json_object import APIJSONObject


class Event(APIJSONObject):
    """Represents a single Box event."""

    _item_type = 'event'
