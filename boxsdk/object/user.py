# coding: utf-8

from __future__ import unicode_literals

from boxsdk.config import API
from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    def get_memberships(self, offset=None, limit=None):
        """
        Get the entries in the user group membership using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The offset of the item at which to begin the response.
        :type offset:
            `str` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the legal hold policy
        :rtype:
            :class:`BoxObjectCollection`
        """
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url='{0}/users/{1}/memberships'.format(API.BASE_API_URL, self.object_id),
            limit=limit,
            offset=offset,
            return_full_pages=False
        )

