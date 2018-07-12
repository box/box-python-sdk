# coding: utf-8

from __future__ import unicode_literals
import json
from .base_object import BaseObject
from boxsdk.config import API
from boxsdk.util.translator import Translator
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection

class Webhook(BaseObject):
    """Represents a Box task."""

    _item_type = 'webhook'
