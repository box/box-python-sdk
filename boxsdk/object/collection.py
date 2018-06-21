# coding: utf-8

from __future__ import unicode_literals

from boxsdk.object.base_object import BaseObject
from boxsdk.pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from boxsdk.util.api_call_decorator import api_call


class Collection(BaseObject):
    """Box API endpoint for interacting with collections."""

    _item_type = 'collection'

    @api_call
    def get_items(self, limit=None, offset=0, fields=None):
        """
        Get the items in a collection using limit-offset paging.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The index at which to start returning items.
        :type offset:
            `int`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the items in the folder.
        :rtype:
            :class:`BoxObjectCollection`
        """
        return LimitOffsetBasedObjectCollection(
            self.session,
            self.get_url('items'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )
