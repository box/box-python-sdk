# coding: utf-8
from typing import Optional, Iterable, TYPE_CHECKING

from boxsdk.object.base_object import BaseObject
from boxsdk.pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from boxsdk.util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class Collection(BaseObject):
    """Box API endpoint for interacting with collections."""

    _item_type = 'collection'

    @api_call
    def get_items(
            self,
            limit: Optional[int] = None,
            offset: int = 0,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the items in a collection using limit-offset paging.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :param offset:
            The index at which to start returning items.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the items in the folder.
        """
        return LimitOffsetBasedObjectCollection(
            self.session,
            self.get_url('items'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )
