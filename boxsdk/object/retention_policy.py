# coding: utf-8
from __future__ import unicode_literals, absolute_import
import json

from .base_object import BaseObject
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call


class RetentionPolicy(BaseObject):
    """Represents a Box retention policy."""
    _item_type = 'retention_policy'

    def get_url(self, *args):
        """
        Returns the url for this retention policy.
        """
        return self._session.get_url('retention_policies', self._object_id, *args)

    @api_call
    def assign(self, assignee, fields=None):
        """Assign a retention policy to a Box item

        :param assignee:
            The item to assign the retention policy on.
        :type assignee:
            :class:`Folder`, :class:`Enterprise`, or :class:`MetadataTemplate`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            A :class:`RetentionPolicyAssignment` object.
        :rtype:
            :class:`RetentionPolicyAssignment`
        """
        url = self._session.get_url('retention_policy_assignments')
        body = {
            'policy_id': self.object_id,
            'assign_to': {
                'type': assignee.object_type,
                'id': assignee.object_id,
            }
        }
        params = {}
        if fields is not None:
            params['fields'] = ','.join(fields)
        response = self._session.post(url, data=json.dumps(body), params=params).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def assignments(self, assignment_type=None, limit=None, marker=None, fields=None):
        """Get the assignments for the retention policy.

        :param assignment_type:
            The type of retention policy assignment to retrieve. Can be set to 'folder', 'enterprise', or 'metadata_template'.
        :type assignment_type:
            `unicode` or None.
        :param limit:
            The maximum number of items to return.
        :type limit:
            `int` or None
        :param marker:
            The position marker at which to begin the response.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterable of assignments in the retention policy.
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if assignment_type is not None:
            additional_params['assignment_type'] = assignment_type
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('assignments'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )
