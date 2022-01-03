# coding: utf-8

from .base_api_json_object import BaseAPIJSONObject


class RecentItem(BaseAPIJSONObject):
    """Represents a single recent item accessed by a Box user."""

    _item_type = 'recent_item'
