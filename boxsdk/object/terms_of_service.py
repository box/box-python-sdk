# coding: utf-8
from __future__ import unicode_literals

import json

from boxsdk.util.text_enum import TextEnum
from .base_object import BaseObject


class TermsOfServiceType(TextEnum):
    """An enum of possible terms of service types"""
    MANAGED = 'managed'
    EXTERNAL = 'external'


class TermsOfServiceStatus(TextEnum):
    """An enum of possible terms of service status"""
    ENABLED = 'enabled'
    DISABLED = 'disabled'


class TermsOfService(BaseObject):
    """Represents a Box terms of service."""

    _item_type = 'terms_of_service'

    def get_user_status(self, user_id=None):
        """
        Get the terms of service user status.

        :param user_id:
            The ID of the user
        :type user_id:
            `str` or None
        :returns:
            A newly created :class:`TermsOfServiceUserStatus` object
        :rtype:
            :class:`TermsOfServiceUserStatus`
        """
        url = self._session.get_url('terms_of_service_user_statuses')
        additional_params = {
            'tos_id': self.object_id,
        }
        if user_id is not None:
            additional_params['user_id'] = user_id
        box_response = self._session.get(url, params=additional_params)
        response_array = box_response.json()
        response = response_array['entries'][0]
        return self.translator.translate('terms_of_service_user_status')(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    def create_user_status(self, is_accepted, user=None):
        """
        Create a terms of service user status.

        :param is_accepted:
            Indicator for whether the terms of service is accepted or not.
        :type is_accepted:
            `boolean`
        :param user:
            The :class:`User` to assign the terms of service to.
        :type user:
            :class:`User` or None
        :returns:
            A newly created :class:`TermsOfServiceUserStatus` object
        :rtype:
            :class:`TermsOfServiceUserStatus`
        """
        url = self._session.get_url('terms_of_service_user_statuses')
        body = {
            'tos': {
                'type': self.object_type,
                'id': self.object_id,
            },
            'is_accepted': is_accepted,
        }
        if user is not None:
            user_json = {
                'type': user.object_type,
                'id': user.object_id,
            }
            body['user'] = user_json
        box_response = self._session.post(url, data=json.dumps(body))
        response = box_response.json()
        return self.translator.translate('terms_of_service_user_status')(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )
