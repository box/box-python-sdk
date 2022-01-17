# coding: utf-8

import copy

from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from boxsdk.session.session import Session
    from boxsdk.util.translator import Translator
    from boxsdk.object.base_object import BaseObject


class Page(Sequence):
    """
    A sequence of BaseObjects that belong to a page returned from a paging api call.

    The Page makes available detailed response data for page requests.
    """
    _item_entries_key_name = "entries"

    def __init__(self, session: 'Session', response_object: dict):
        """
        :param session:
            The Box session used to make the request that generated the response.
        :param response_object:
            The parsed HTTP response from Box after requesting more pages.
        """
        super().__init__()
        self._session = session
        self._response_object = response_object

    @property
    def _translator(self) -> 'Translator':
        """
        The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.
        """
        return self._session.translator

    @property
    def response_object(self) -> dict:
        """
        Return a copy of the response object for this Page.
        """
        return copy.deepcopy(self._response_object)

    def __getitem__(self, key: str) -> 'BaseObject':
        """
        Try to get the attribute from the API response object.

        :param key:
            The attribute to retrieve from the API response object.
        """
        item_json = self._response_object[self._item_entries_key_name][key]
        return self._translator.translate(self._session, item_json)

    def __len__(self) -> int:
        """
        Get the number of items in the page.
        """
        return len(self._response_object[self._item_entries_key_name])
