# coding: utf-8
from __future__ import unicode_literals

import json

from boxsdk.util.text_enum import TextEnum
from boxsdk.exception import BoxAPIException
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

    def get_user_status(self, user=None):
        """
        Get the terms of service user status.

        :param user:
            This is the user to get the status of the terms of service for. This defaults to current
            user.
        :type user:
            :class:`User` or None
        :returns:
            A :class:`TermsOfServiceUserStatus` object
        :rtype:
            :class:`TermsOfServiceUserStatus`
        """
        url = self._session.get_url('terms_of_service_user_statuses')
        additional_params = {
            'tos_id': self.object_id,
        }
        if user is not None:
            additional_params['user_id'] = user.object_id
        box_response = self._session.get(url, params=additional_params)
        response_object = box_response.json()
        response = response_object['entries'][0]
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    def accept(self, user=None):
        """
        Accept a terms of service.

        :param user:
            The :class:`User` to assign the terms of service to.
        :type user:
            :class:`User` or None
        :returns:
            A newly created :class:`TermsOfServiceUserStatus` object
        :rtype:
            :class:`TermsOfServiceUserStatus`
        """
        return self.set_user_status(is_accepted=True, user=user)

    def reject(self, user=None):
        """
        Reject a terms of service.

        :param user:
            The :class:`User` to assign the terms of service to.
        :type user:
            :class:`User` or None
        :returns:
            A newly created :class:`TermsOfServiceUserStatus` object
        :rtype:
            :class:`TermsOfServiceUserStatus`
        """
        return self.set_user_status(is_accepted=False, user=user)

    def set_user_status(self, is_accepted, user=None):
        """
        Create a terms of service user status.

        :param is_accepted:
            Indicates whether a use has accepted or rejected a terms of service.
        :type is_accepted:
            `bool`
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
            body['user'] = {
                'type': user.object_type,
                'id': user.object_id,
            }
        translated_response = None
        try:
            box_response = self._session.post(url, data=json.dumps(body))
            response = box_response.json()
            translated_response = self.translator.translate(
                session=self._session,
                response_object=response,
            )
        except BoxAPIException as err:
            if err.status == 409:
                user_status = self.get_user_status(user)
                translated_response = user_status.update_info({'is_accepted': is_accepted})
        return translated_response
