# coding: utf-8

from __future__ import unicode_literals

import json

from .base_object import BaseObject
from boxsdk.util.translator import Translator
from ..config import API

class LegalHoldPolicy(BaseObject):
    """Represents a Box legal_hold_policy"""

    _item_type = 'legal_hold_policy'

    def get_url(self, *args):
        return self._session.get_url('legal_hold_policies', self._object_id, *args)

    def assign(self, item):
        url = self._session.get_url('legal_hold_policy_assignments')
        body = {
            'policy_id': self.object_id,
            'assign_to': {
                'type': item.object_type,
                'id': item.object_id
            }
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return Translator().translate(response['type'])(
            self._session,
            response['id'],
            response,
        ) 
