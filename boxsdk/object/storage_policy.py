# coding:utf-8
from __future__ import unicode_literals, absolute_import

import json

from .base_object import BaseObject


class StoragePolicy(BaseObject):
    """Represents the storage policy"""

    _item_type = 'storage_policy'

    def get_url(self, *args):
        """
        Get url for storage policies.
        """
        return self._session.get_url('storage_policies', self._object_id, *args)

    def assign(self, user):
        """
        Checks to see if a user is already assigned a storage policy or if the storage policy assigned
        to user belongs to the enterprise. If neither, then update the user storage policy to the new one.

        :param user:
            The class:`User` to assign the storage policy to
        :type user:
            :class:`User`
        :returns:
            Information about the :class:`StoragePolicyAssignment` object.
        :rtype:
            :class:`StoragePolicyAssignment`
        """
        assignment = user.get_storage_policy_assignment()
        if assignment.id == self.object_id:
            return assignment

        if assignment.assigned_to['type'] == 'enterprise':
            return self.create_assignment(user)

        update_object = {
            'storage_policy': {
                'type': self.object_type,
                'id': self.object_id,
            },
        }
        return assignment.update_info(update_object)

    def create_assignment(self, user):
        """
        Assign a storage policy to a :class:`User`.

        :param user:
            The :class:'User` to assign the storage policy to.
        :type:
            :class:`User`
        :returns:
            Information about the :class:`StoragePolicyAssignment` object
        :rtype:
            :class:`StoragePolicyAssignment`
        """
        url = self._session.get_url('storage_policy_assignments')
        body = {
            'storage_policy': {
                'type': 'storage_policy',
                'id': self.object_id,
            },
            'assigned_to': {
                'type': user.object_type,
                'id': user.object_id,
            }
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )
