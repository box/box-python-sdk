# coding: utf-8

from __future__ import unicode_literals

from boxsdk.object.base_api_json_object import BaseAPIJSONObject


class Event(BaseAPIJSONObject):
    """Represents a single Box event"""

    _item_type = 'event'
