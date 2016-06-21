# coding: utf-8

from __future__ import unicode_literals, absolute_import
from collections import Mapping
from abc import ABCMeta
import six

from .base_api_json_object import BaseAPIJSONObject, BaseAPIJSONObjectMeta


class APIJSONObjectMeta(BaseAPIJSONObjectMeta, ABCMeta):
    """
    Avoid conflicting metaclass definitions for APIJSONObject.
    http://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
    """
    pass


class APIJSONObject(six.with_metaclass(APIJSONObjectMeta, BaseAPIJSONObject, Mapping)):
    """Class representing objects that are not part of the REST API."""

    def __len__(self):
        return len(self._response_object)

    def __iter__(self):
        return iter(self._response_object)
