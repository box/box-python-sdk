# coding: utf-8

from __future__ import unicode_literals

import json

from .base_object import BaseObject
from boxsdk.config import API
from boxsdk.util.translator import Translator
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


class Task(BaseObject):
    """Represents a Box task."""

    _item_type = 'task'

    def assign(self, assign_to_id=None, assign_to_login=None):
        url = self._session.get_url('task_assignments')
        body = {
            'task': {
                'type': 'task',
                'id': self.object_id
            },
            'assign_to': {
                'id': assign_to_id,
                'login': assign_to_login
            }
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return Translator().translate(response['type'])(
            self._session,
            response['id'],
            response,
        )

