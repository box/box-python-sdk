# coding: utf-8

from __future__ import unicode_literals

import json

from .base_object import BaseObject
from boxsdk.config import API


class Task(BaseObject):
    """Represents a Box task."""

    _item_type = 'task'

    # def get_assignment

