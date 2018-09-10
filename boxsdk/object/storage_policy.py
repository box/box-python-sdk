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

    def assign(self, assignee):
        """
        Assign a storage policy to a `user` or `enterprise`

        :param assignee:
            The `user` or `enterprise` to assign the storage policy to
        :type:
            :class:User
        """
        url = self._session.get_url('storage_policy_assignments')
        body = {
            'storage_policy': {
                'type': 'storage_policy',
                'id': self.object_id,
            },
            'assigned_to': {
                'type': assignee.object_type,
                'id': assignee.object_id,
            }
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(response['type'])(
            self._session,
            response['id'],
            response,
        )
