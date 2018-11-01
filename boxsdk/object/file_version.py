# coding: utf-8
from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject


class FileVersion(BaseObject):
    """Represents a Box file version."""
    _item_type = 'file_version'
