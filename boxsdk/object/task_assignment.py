# coding: utf-8

from __future__ import unicode_literals, absolute_import

import json
from .base_object import BaseObject
from boxsdk.util.text_enum import TextEnum

from boxsdk.config import API


class ResolutionState(TextEnum):
    """An enum of possible resolution states"""
    COMPLETED = 'completed'
    INCOMPLETE = 'incomplete'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class TaskAssignment(BaseObject):
    """Represents a Box task."""

    _item_type = 'task_assignment'
