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

    def update(self, is_accepted):
        """
        Update the user status on a term of service.

        :param is_accepted:
            Indicates whether the terms of service has been accepted or not.
        :type is_accepted:
            `boolean`
        """
        url = '{0}/terms_of_service_user_statuses/{1}'.format(API.BASE_API_URL, self.object_id)
        body = {
            'is_accepted': is_accepted
        }
        response = self._session.put(url, data=json.dumps(body)).json()
        return Translator().translate(response['type'])(
            self._session,
            response['id'],
            response,
        )

