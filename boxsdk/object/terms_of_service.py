# coding: utf-8
from __future__ import unicode_literals
from functools import partial

import json

from boxsdk.config import API
from .base_object import BaseObject
from .terms_of_service_user_status import TermsOfServiceUserStatus
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


class TermsOfService(BaseObject):
    """Represents a Box terms of service."""

    _item_type = 'terms_of_service'

    def get_user_status(self, user_id=None, limit=None, fields=None):
        """
        Get the entries in the terms of service user status using limit-offset paging.
        :param user_id:
            The ID of the user
        :type user_id:
            `str` or None
        :returns:
            An iterator of the entries in the terms of service user status
        """
        if limit is not None:
            additional_params['limit'] = limit
        additional_params = {
            'tos_id': self.object_id,
            'user_id': user_id,
        }
        return MarkerBasedObjectCollection(
            session=self._session,
            url='{0}/terms_of_service_user_statuses'.format(API.BASE_API_URL),
            additional_params=additional_params,
            limit=limit,
            marker=None,
            fields=fields,
            return_full_pages=False
        )

    def create_user_status(self, is_accepted, user):
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
        url = self.get_url('terms_of_service_user_statuses')
        body = {
            'tos': {
                'type': self.type,
                'id': self.object_id,
            },
            'user': {
                'type': user.type,
                'id': user.object_id,
            },
            'is_accepted': is_accepted,
        }
        box_response = self._session.post(url, data=json.dumps(body))
        response = box_response.json()
        return self.translator.translate('terms_of_service_user_status')(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )
