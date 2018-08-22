# coding: utf-8

from __future__ import unicode_literals, absolute_import

import json
from .base_object import BaseObject

from boxsdk.config import API

class TaskAssignment(BaseObject):
    """Represents a Box task."""

    _item_type = 'task_assignment'
