# coding: utf-8

from __future__ import unicode_literals, absolute_import

import sys
from abc import ABCMeta

from .base_api_json_object import BaseAPIJSONObject, BaseAPIJSONObjectMeta
from ..util.compat import with_metaclass

if sys.version_info >= (3, 3):
    from collections.abc import Mapping  # pylint:disable=no-name-in-module,import-error
else:
    from collections import Mapping  # pylint:disable=no-name-in-module,import-error


class APIJSONObjectMeta(BaseAPIJSONObjectMeta, ABCMeta):
    """
    Avoid conflicting metaclass definitions for APIJSONObject.
    http://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
    """
    pass


class APIJSONObject(with_metaclass(APIJSONObjectMeta, BaseAPIJSONObject, Mapping)):
    """Class representing objects that are not part of the REST API."""

    def __len__(self):
        return len(self._response_object)
