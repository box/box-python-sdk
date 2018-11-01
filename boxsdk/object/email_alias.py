# coding: utf-8
from __future__ import unicode_literals

from .base_object import BaseObject


class EmailAlias(BaseObject):
    """Represents a Box email alias."""

    _item_type = 'email_alias'
