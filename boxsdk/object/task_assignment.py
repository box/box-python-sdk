# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject


class TaskAssignment(BaseObject):
    """Represents a Box task assignment."""

    _item_type = 'task_assignment'
