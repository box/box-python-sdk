# coding: utf-8

from __future__ import unicode_literals, absolute_import

from collections import Sequence
import copy

from boxsdk.object.base_object import BaseObject
from boxsdk.object.base_endpoint import BaseEndpoint
from boxsdk.util.translator import Translator


class Page(Sequence, object):
    """
    A sequence of BaseObjects that belong to a page returned from a paging api call.

    The Page makes available detailed response data for page requests.
    """
    _item_entries_key_name = "entries"

    def __init__(self, session, response_object):
        """
        :param session:
            The Box session used to make the request that generated the response.
        :type session:
            :class:`BoxSession`
        :param response_object:
            The parsed HTTP response from Box after requesting more pages.
        :type response_object:
            `dict`
        """
        super(Page, self).__init__()
        self._session = session
        self._response_object = response_object

    @property
    def _translator(self):
        """The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.

        :rtype:   :class:`Translator`
        """
        return Translator()

    @property
    def response_object(self):
        """
        Return a copy of the response object for this Page.

        :rtype: `dict`
        """
        return copy.deepcopy(self._response_object)

    def __getitem__(self, key):
        """
        Try to get the attribute from the API response object.

        :param key:
            The attribute to retrieve from the API response object.
        :type key:
            `unicode`
        :rtype:
            :class:`BaseObject`
        """
        item_json = self._response_object[self._item_entries_key_name][key]
        item_class = self._translator.translate(item_json['type'])
        kwargs = {}
        if issubclass(item_class, BaseObject):
            kwargs['object_id'] = item_json['id']
        if issubclass(item_class, BaseEndpoint):
            kwargs['session'] = self._session

        item = item_class(response_object=item_json, **kwargs)
        return item

    def __len__(self):
        """
        Get the number of items in the page.

        :rtype:
            `int`
        """
        return len(self._response_object[self._item_entries_key_name])
