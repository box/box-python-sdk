# coding: utf-8

from __future__ import unicode_literals, absolute_import

from boxsdk.util.text_enum import TextEnum
from .base_object import BaseObject


class ResolutionState(TextEnum):
    """An enum of possible resolution states"""
    COMPLETED = 'completed'
    INCOMPLETE = 'incomplete'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class TaskAssignment(BaseObject):
    """Represents a Box task."""

    _item_type = 'task_assignment'
