# coding: utf-8

from __future__ import unicode_literals

from .base_object import BaseObject


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    def get_storage_policy_assignment(self):
        """
        Get the entries in the storage policy assignment using limit-offset paging.

        :returns:
            The :class:`StoragePolicyAssignment` object information
        :rtype:
            :class:`StoragePolicyAssignment`
        """
        url = self._session.get_url('storage_policy_assignments')
        additional_params = {
            'resolved_for_type': 'user',
            'resolved_for_id': self.object_id,
        }
        box_response = self._session.get(url, params=additional_params)
        response = box_response.json()['entries'][0]
        return self.translator.translate('storage_policy_assignment')(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )
