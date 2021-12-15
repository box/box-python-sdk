# coding: utf-8

from .api_json_object import APIJSONObject


class Watermark(APIJSONObject):
    """Box API endpoint for applying watermark in a Box account."""

    _item_type = 'watermark'
