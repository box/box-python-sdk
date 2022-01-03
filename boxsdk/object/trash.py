# coding: utf-8
import json
from typing import Iterable, TYPE_CHECKING, Optional

from .base_endpoint import BaseEndpoint
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.object.item import Item
    from boxsdk.object.folder import Folder
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class Trash(BaseEndpoint):
    """Box API endpoint for performing trash related actions in Box."""

    @api_call
    def get_item(self, item: 'Item', fields: Iterable[str] = None) -> 'Item':
        """
        Get item from trash.

        :param item:
            The :class:`Item` object to get info on.
        :param fields:
            List of fields to request
        :returns:
            Information for a trashed :class:`Item` object.
        """
        url = item.get_url('trash')
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def restore_item(
            self,
            item: 'Item',
            name: Optional[str] = None,
            parent_folder: Optional['Folder'] = None,
            fields: Iterable[str] = None
    ) -> 'Item':
        """
        Restores an item from the trash. Could be files, folders, or weblinks.

        :param item:
            The :class:`Item` object to restore from trash.
        :param name:
            The new name for this item. Only used if the item can't be restored due to name conflict.
        :param parent_folder:
            The new parent folder. Only used if the previous parent folder no longer exists.
        :param fields:
            List of fields to request
        :returns:
            A restored :class:`Item`.
        """
        url = item.get_url()
        body = {}
        if name is not None:
            body['name'] = name
        if parent_folder is not None:
            body['parent'] = {'id': parent_folder.object_id}
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        box_response = self._session.post(url, data=json.dumps(body), params=params)
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def permanently_delete_item(self, item: 'Item') -> bool:
        """
        Permanently delete an item that is in the trash. The item will no longer exist in Box.

        :param item:
            The :class:`Item` to delete from trash.
        :returns:
            Whether or not the delete was successful.
        """
        url = item.get_url('trash')
        box_response = self._session.delete(url, expect_json_response=False)
        return box_response.ok

    @api_call
    def get_items(self, limit: Optional[int] = None, offset: Optional[int] = None, fields: Iterable[str] = None) -> 'BoxObjectCollection':
        """
        Using limit-offset paging, get the files, folders and web links that are in the user's trash.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param offset:
            The offset of the item at which to begin the response.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the trash
        """
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('folders', 'trash', 'items'),
            limit=limit,
            offset=offset,
            fields=fields,
            return_full_pages=False,
        )
