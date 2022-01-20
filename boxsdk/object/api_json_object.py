# coding: utf-8

from abc import ABCMeta
from collections.abc import Mapping

from .base_api_json_object import BaseAPIJSONObject, BaseAPIJSONObjectMeta


class APIJSONObjectMeta(BaseAPIJSONObjectMeta, ABCMeta):
    """
    Avoid conflicting metaclass definitions for APIJSONObject.
    http://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
    """


class APIJSONObject(BaseAPIJSONObject, Mapping, metaclass=APIJSONObjectMeta):
    """Class representing objects that are not part of the REST API."""

    def __len__(self) -> int:
        return len(self._response_object)
