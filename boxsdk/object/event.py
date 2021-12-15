# coding: utf-8

from .api_json_object import APIJSONObject


class Event(APIJSONObject):
    """Represents a single Box event."""

    _item_type = 'event'
