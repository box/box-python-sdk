# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject


class Comment(BaseObject):
    """Represents a Box file comment."""

    _item_type = 'comment'
