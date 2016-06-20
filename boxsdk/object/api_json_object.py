# coding: utf-8

from __future__ import unicode_literals, absolute_import
from collections import Mapping

# import six

from .base_api_json_object import BaseAPIJSONObject, BaseAPIJSONObjectMeta


class APIJSONObjectMeta(BaseAPIJSONObjectMeta, Mapping.__metaclass__):
    """Avoid conflicting metaclass definitions for APIJSONObject"""
    pass


# @six.add_metaclass(APIJSONObjectMeta)
# class APIJSONObject(APIJSONObjectMeta, BaseAPIJSONObject, Mapping):
class APIJSONObject(BaseAPIJSONObject, Mapping):
    """Class representing objects that are not part of the REST API."""

    __metaclass__ = APIJSONObjectMeta

    def __len__(self):
        return len(self._response_object)

    def __iter__(self):
        return self._response_object.__iter__()
