# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from .base_object import BaseObject


class TermsOfServiceUserStatus(BaseObject):
    """Represents a Box terms of service user status."""

    _item_type = 'terms_of_service_user_status'
