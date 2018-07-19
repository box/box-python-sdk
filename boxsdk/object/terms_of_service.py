# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from boxsdk.config import API
from .base_object import BaseObject
from .terms_of_service_user_status import TermsOfServiceUserStatus



class TermsOfService(BaseObject):
    """Represents a Box terms of service."""

    _item_type = 'terms_of_service'


    def create_user_status(self, is_accepted, user=None):
        """
        Create a terms of service user status.

        :param is_accepted:
            Indicator for whether the terms of service is accepted or not.
        :type is_accepted:
            `boolean`
        :param user:
            The user to assign the terms of service to.
        :type user:
            `unicode` or None
        """
        url = '{0}/terms_of_services_user_statuses'.format(API.BASE_API_URL)
        body = {
            'tos': {
                'type': self.type,
                'id': self.object_id
            },
            'user': {
                'type': user.type,
                'id': user.object_id
            },
            'is_accepted': is_accepted
        }
        box_response = self._session.post(url, data=json.dumps(body))
        response = box_response.json()
        return TermsOfServiceUserStatus(self._session, response['id'], response)

    