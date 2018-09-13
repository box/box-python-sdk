# coding: utf-8
from __future__ import unicode_literals
from functools import partial

import json

from ..config import API
from .base_object import BaseObject
from ..util.translator import Translator


class TermsOfServiceUserStatus(BaseObject):
    """Represents a Box terms of service user status."""

    _item_type = 'terms_of_service_user_status'

    def get_url(self, *args):
        return self._session.get_url('terms_of_service_user_statuses', self._object_id, *args)

    def accept(self):
        """
        Accept a term of service.
        """
        body = {
            'is_accepted': True
        }
        return self.update_info(data=body)

    def reject(self):
        """
        Reject a term of service.
        """
        body = {
            'is_accepted': False
        }
        return self.update_info(data=body)
