# coding: utf-8
from __future__ import unicode_literals

import json

from .base_object import BaseObject
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call


class LegalHoldPolicy(BaseObject):
    """Represents a Box legal_hold_policy"""

    _item_type = 'legal_hold_policy'

    def get_url(self, *args):
        return self._session.get_url('legal_hold_policies', self._object_id, *args)

    @api_call
    def assign(self, assignee):
        """Assign legal hold policy

        :param assignee:
            The `file_version`, `file`, `folder`, or `user` to assign the legal hold policy to.
        :type assignee:
            :class:`FileVersion` :class:`File` or :class:`Folder` or :class:`User`
        :returns:
            A legal hold policy assignment object
        :rtype:
            :class:`LegalHoldPolicyAssignment`
        """
        url = self._session.get_url('legal_hold_policy_assignments')
        body = {
            'policy_id': self.object_id,
            'assign_to': {
                'type': assignee.object_type,
                'id': assignee.object_id
            }
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            self._session,
            response,
        )

    @api_call
    def get_assignments(self, assign_to_type=None, assign_to_id=None, limit=None, marker=None, fields=None):
        """
        Get the entries in the legal hold policy assignment using limit-offset paging.

        :param assign_to_type:
            Filter assignments of this type only. Can be `file_version`, `file`, `folder`, or `user`
        :type assign_to_type:
            `unicode` or None
        :param assign_to_id:
            Filter assignments to this ID only
        :type assign_to_id:
            `unicode` or None
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the legal hold policy assignment
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {
            'policy_id': self.object_id,
        }
        if assign_to_type is not None:
            additional_params['assign_to_type'] = assign_to_type
        if assign_to_id is not None:
            additional_params['assign_to_id'] = assign_to_id
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('legal_hold_policy_assignments'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def get_file_version_legal_holds(self, limit=None, marker=None, fields=None):
        """
        Get legal holds for a file version.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the file version legal holds
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {
            'policy_id': self.object_id,
        }
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('file_version_legal_holds'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )
