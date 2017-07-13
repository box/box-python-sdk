# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from .base_object import BaseObject
from ..config import API
from ..util.api_call_decorator import api_call


class Collection(BaseObject):
    """Represents a single Box collection."""

    _item_type = 'collection'

    @api_call
    def add_item(self, item):
        """
        Add an item to this collection.

        :param item:
            The Item to add to the collection
        :type item:
            :class:`Item`
        :returns:
            The new Item instance
        :rtype:
            :class:`Item`
        """
        return item.add_to_collection(self)

    @api_call
    def remove_item(self, item):
        """
        Remove an item from this collection. Only the favorites collection is supported, so all collections are removed.

        :param item:
            The Item to remove from the collection
        :type item:
            :class:`Item`
        :returns:
            The new Item instance
        :rtype:
            :class:`Item`
        """
        return item.remove_from_collection(self)

    @api_call
    def get_items(self, limit=100, offset=0, fields=None):
        """Get the items in this collection.

        :param limit:
            The maximum number of items to return.
        :type limit:
            `int`
        :param offset:
            The index at which to start returning items.
        :type offset:
            `int`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            A list of items in the collection.
        :rtype:
            `list` of :class:`Item`
        """
        url = self.get_url('items')
        params = {
            'limit': limit,
            'offset': offset,
        }
        if fields:
            params['fields'] = ','.join(fields)
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return [self.translator.translate(item['type'])(self._session, item['id'], item) for item in response['entries']]
