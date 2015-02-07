# coding: utf-8

from __future__ import unicode_literals

from .base_object import BaseObject


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'
