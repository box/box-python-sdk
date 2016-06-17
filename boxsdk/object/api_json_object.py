# coding: utf-8

from __future__ import unicode_literals
from collections import Mapping

from boxsdk.object.base_api_json_object import BaseAPIJSONObject


class APIJSONObject(BaseAPIJSONObject, Mapping):
    """Class representing objects that are not part of the REST API"""

    pass
