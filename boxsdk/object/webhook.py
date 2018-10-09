# coding: utf-8
from __future__ import unicode_literals

from .base_object import BaseObject


class Webhook(BaseObject):
    """Represents a Box Webhook."""

    _item_type = 'webhook'
