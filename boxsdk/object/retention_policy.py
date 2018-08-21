# coding: utf-8
from __future__ import unicode_literals, absolute_import
import json

from .base_object import BaseObject
from boxsdk.util.translator import Translator
from ..config import API
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


class RetentionPolicy(BaseObject):
    """Represents a Box retention policy."""
    _item_type = 'retention_policy'

    def get_url(self, *args):
        """
        Returns the url for this retention policy.
        """
        return self._session.get_url('retention_policies', self._object_id, *args)

    def assign(self, item, fields=None):
        """Assign a retention policy to a Box item
        :param item:
            The item to assign the retention policy on.
        :type item:
            `object`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        """
        url = self._session.get_url('retention_policy_assignments')
        body = {
            'policy_id': self.object_id,
            'assign_to': {
                'type': item.object_type,
                'id': item.object_id,
            }
        }
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        response = self._session.post(url, data=json.dumps(body), params=params).json()
        return Translator().translate(response['type'])(
            self._session,
            response['id'],
            response,
        )

    def assignments(self, assignment_type=None, limit=None, marker=None, fields=None):
        """Get the assignments for the retention policy.
        :param limit:
            The maximum number of items to return.
        :type limit:
            `int`
        :param marker:
            The position marker at which to begin the response.
        :type marker:
            `unicode`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterable of assignments in the retention policy.
        :rtype:
            `Iterable` of :class:`RetentionPolicyAssignment`
        """
        additional_params = {
            'type': assignment_type,
        }
        return MarkerBasedObjectCollection(
            session=self._session,
            url='{0}/retention_policies/{1}/assignments'.format(API.BASE_API_URL, self.object_id),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )
