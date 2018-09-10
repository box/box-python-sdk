# coding: utf-8

from __future__ import unicode_literals

from .base_object import BaseObject


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    def storage_policy_assignments(self, limit=None, marker=None, fields=None):
        """
        Get the entries in the storage policy assignment using limit-offset paging.

        :param limit:
            The number of entries to retrieve.
        :type limit:
            `unicode` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `str` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the storage policy assignment
        :rtype:
            :class:`BoxObjectCollection`
        """
        url = self._session.get_url('storage_policy_assignments')
        additional_params = {
            'resolved_for_type': 'user',
            'resolved_for_id': self.object_id,
        }
        box_response = self._session.get(url, params=additional_params)
        response = box_response.json()
        return self.translator.translate('storage_policy_assignment')(
            session=self._session,
            object_id=response['entries'][0]['id'],
            response_object=response['entries'][0],
        )
