# coding: utf-8

from __future__ import unicode_literals, absolute_import

import copy
import sys

if sys.version_info >= (3, 3):
    from collections.abc import Sequence  # pylint:disable=no-name-in-module,import-error
else:
    from collections import Sequence  # pylint:disable=no-name-in-module,import-error


class Page(Sequence):
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
        return self._session.translator

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
        return self._translator.translate(self._session, item_json)

    def __len__(self):
        """
        Get the number of items in the page.

        :rtype:
            `int`
        """
        return len(self._response_object[self._item_entries_key_name])
