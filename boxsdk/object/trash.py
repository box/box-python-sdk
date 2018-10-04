# coding: utf-8
from __future__ import unicode_literals, absolute_import

import json

from .base_endpoint import BaseEndpoint
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection


class Trash(BaseEndpoint):
    """Box API endpoint for performing trash related actions in Box."""

    def get_from_trash(self, item, fields=None):
        """
        Get item from trash.

        :param item:
            The :class:`File` or :class:`Folder` or :class:`WebLink` object to restore from trash.
        :type item:
            :class:`File` or :class:`Folder` or :class:`WebLink`.
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            A `dict` containing the trashed file, folder or weblink.
        :rtype:
            `dict`
        """
        url = self._session.get_url(item.object_type + 's', item.object_id, 'trash')
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return response

    def restore_from_trash(self, item, name=None, parent_id=None, fields=None):
        """
        Restores an item from the trash. Could be files, folders, or weblinks.

        :param item:
            The :class:`File` or :class:`Folder` or :class:`WebLink` object to restore from trash.
        :type item:
            :class:`File` or :class:`Folder` or :class:`WebLink`.
        :param name:
            The new name for this item. Only used if the item can't be restored due to name conflict.
        :type name:
            `unicode` or None
        :param parent_id:
            The id of the new parent folder. Only used if the previous parent folder no longer exists.
        :type parent_id:
            `unicode` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            A `dict` containing the restored file, folder or weblink.
        :rtype:
            `dict`
        """
        url = self._session.get_url(item.object_type + 's', item.object_id)
        body = {}
        if name is not None:
            body['name'] = name
        if parent_id is not None:
            body['parent'] = {'id': parent_id}
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        box_response = self._session.post(url, data=json.dumps(body), params=params)
        response = box_response.json()
        return response

    def permanently_delete_item(self, item):
        """
        Permanently delete an item that is in the trash. The item will no longer exist in Box.
        """
        url = self._session.get_url(item.object_type + 's', item.object_id, 'trash')
        box_response = self._session.delete(url, expect_json_response=False)
        return box_response.ok

    def get_trashed_items(self, limit=None, offset=None, fields=None):
        """
        Using limit-offset paging, get the files, folders and web links that are in the user's trash.

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
            An iterator of the entries in the trash
        :rtype:
            :class:`BoxObjectCollection`
        """
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('folders', 'trash', 'items'),
            limit=limit,
            offset=offset,
            fields=fields,
            return_full_pages=False,
        )
