# coding: utf-8
from .base_object import BaseObject


class EmailAlias(BaseObject):
    """Represents a Box email alias."""

    _item_type = 'email_alias'
