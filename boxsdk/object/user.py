# coding: utf-8

from __future__ import unicode_literals

from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..util.api_call_decorator import api_call


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    @api_call
    def get_group_memberships(self, limit=None, offset=None, fields=None):
        """
        Get the entries in the user group membership using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The offset of the item at which to begin the response.
        :type offset:
            `int` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the groups
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if fields is not None:
            additional_params['fields'] = ','.join(fields)
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url=self.get_url('memberships'),
            additional_params=additional_params,
            limit=limit,
            offset=offset,
            return_full_pages=False,
        )
