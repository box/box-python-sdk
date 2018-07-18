# coding: utf-8

from __future__ import unicode_literals

import json

from .base_object import BaseObject
from boxsdk.util.translator import Translator
from ..config import API
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection

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

    def get_assignments(self, assign_to_type=None, assign_to_id=None, limit=None, marker=None, fields=None):
        """
        Get the entries in the legal hold policy assignment using limit-offset paging.

        :param policy_id:
            The ID of the legal hold policy assignment
        :type policy_id:
            `str` or None
        :param assign_to_type:
            Filter assignments of this type only. Can be `file_version`, `file`, `folder`, or `user`
        :type assign_to_type:
            `str` or None
        :param assign_to_id:
            Filter assignments to this ID only
        :type assign_to_id:
            `str` or None
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `str` or None
        :param marker:
            The paging marker to start paging from
        :type marker:
            `str` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the legal hold policy assignment
        """
        additional_params = {
            'policy_id': self.object_id,
            'assign_to_type': assign_to_type,
            'assign_to_id': assign_to_id,
        }
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('legal_hold_policy_assignments'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False
        )
