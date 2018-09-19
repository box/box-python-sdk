# coding: utf-8
from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject


class WebLink(BaseObject):
    """Box API endpoint for interacting with WebLinks."""

    _item_type = 'web_link'
