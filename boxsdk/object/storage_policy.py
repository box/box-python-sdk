# coding:utf-8

from __future__ import unicode_literals, absolute_import

import json

from .base_object import BaseObject
from boxsdk.util.translator import Translator


class StoragePolicy(BaseObject):
    """Represents the storage policy"""

    def get_url(self, *args):
        return self._session.get_url('storage_policies', self._object_id, *args)

    _item_type = 'storage_policy'


    def assign(self, item):
        url = self._session.get_url('storage_policy_assignments')
        body = {
            'storage_policy': {
                'type': 'storage_policy',
                'id': self.object_id
            },
            'assigned_to': {
                'type': item.type,
                'id': item.object_id
            }
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return Translator().translate(response['type'])(
            self._session,
            response['id'],
            response,
        )

