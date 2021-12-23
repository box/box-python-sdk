# coding: utf-8

import json
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING, Optional, Union, Any, Iterator as Iter
from boxsdk.pagination.page import Page

if TYPE_CHECKING:
    from boxsdk.session.session import Session
    from boxsdk.object.base_object import BaseObject


class BoxObjectCollection(Iterator, ABC):
    """
    An iterator that represents a collection of Box objects (BaseObject).

    A BoxObjectCollection instance contains everything it needs in order to retrieve and page through
    responses from Box API endpoints that return collections of Box objects.

    This class only has two public methods:

    1). next(), which returns either a Page (sequence of BaseObjects) or individual BaseObjects based on
    the constructor argument 'return_full_pages'.

    2). next_pointer(), which returns the pointer (either an offset or a marker, based on the endpoint) that
    will be used to retrieve the next page of Box objects. This pointer can be used when requesting new
    BoxObjectCollection instances that start off from a particular page, instead of from the very beginning.
    """
    _page_constructor = Page

    def __init__(
            self,
            session: 'Session',
            url: str,
            limit: Optional[int] = None,
            fields: Optional[Iter[str]] = None,
            additional_params: Optional[dict] = None,
            return_full_pages: bool = False,
            use_post: bool = False
    ):
        """
        :param session:
            The Box session used to make requests.
        :param url:
            The endpoint url to hit.
        :param limit:
            The number of entries for each page to return. The default, as well as the upper limit of this value,
            differs by endpoint. See https://developer.box.com/en/reference. If limit is set to None, then the default
            limit (returned by Box in the response) is used.
        :param fields:
            List of fields to request. If None, will return the default fields for the object.
        :param additional_params:
            Additional HTTP params to send in the request.
        :param return_full_pages:
            If True, then the returned iterator for this collection will return full pages of Box objects on each
            call to next(). If False, the iterator will return a single Box object on each next() call.
        :param use_post:
            If True, then the returned iterator will make POST requests with all the data in the body on each
            call to next().
            If False, the iterator will make GET requets with all the data as query params on each call to next().
        """
        super().__init__()
        self._session = session
        self._url = url
        self._limit = limit
        self._fields = fields
        self._additional_params = additional_params
        self._return_full_pages = return_full_pages
        self._has_retrieved_all_items = False
        self._all_items = None
        self._use_post = use_post

    def next(self) -> Union[Page, 'BaseObject']:
        """
        Returns either a Page (a Sequence of BaseObjects) or a BaseObject depending on self._return_full_pages.

        Invoking this method may make an API call to Box. Any exceptions that can occur while making requests
        may be raised in this method.
        """
        if self._all_items is None:
            self._all_items = self._items_generator()
        return next(self._all_items)

    __next__ = next

    def _items_generator(self) -> Union[Page, 'BaseObject']:
        while not self._has_retrieved_all_items:
            response_object = self._load_next_page()

            self._update_pointer_to_next_page(response_object)
            self._has_retrieved_all_items = not self._has_more_pages(response_object)
            page = self._page_constructor(self._session, response_object)

            if self._return_full_pages:
                yield page
            else:
                # It's possible for the Box API to return 0 items in a page, even if there are more items to be
                # retrieved on subsequent pages. When self._return_full_pages is True, then yielding a 0-item
                # page is fine because that's what the page returned.
                # But when we are iterating over individual items, and not pages, it's odd to yield a sequence of
                # Nones (for that page that had 0 items). So instead, we continue to request more pages until we
                # have Box objects to yield.
                if not page:
                    continue
                for entry in page:
                    yield entry

    def _load_next_page(self) -> dict:
        """
        Request the next page of entries from Box. Raises any network-related exceptions, including BoxAPIException.
        Returns a parsed dictionary of the JSON response from Box
        """
        params = {}
        if self._limit is not None:
            params['limit'] = self._limit
        if self._additional_params:
            params.update(self._additional_params)
        params.update(self._next_page_pointer_params())
        if self._use_post:
            if self._fields:
                params['fields'] = self._fields
            box_response = self._session.post(self._url, data=json.dumps(params), headers={b'Content-Type': b'application/json'})
        else:
            if self._fields:
                params['fields'] = ','.join(self._fields)
            box_response = self._session.get(self._url, params=params)
        return box_response.json()

    @abstractmethod
    def _update_pointer_to_next_page(self, response_object: dict) -> None:
        """
        Update the internal pointer attribute of this class to what will be used to request the next page
        of Box objects.

        A "pointer" can either be a marker (for marker-based paging) or an offset (for limit-offset paging).

        :param response_object:
            The parsed HTTP response from Box after requesting more pages.
        """
        raise NotImplementedError

    @abstractmethod
    def _has_more_pages(self, response_object: dict) -> bool:
        """
        Are there more pages of entries to query Box for? This gets invoked after self._update_pointer_to_next_page().

        :param response_object:
            The parsed HTTP response from Box after requesting more pages.
        """
        raise NotImplementedError

    @abstractmethod
    def _next_page_pointer_params(self) -> dict:
        """
        The dict of HTTP params that specify which page of Box objects to retrieve.
        """
        raise NotImplementedError

    @abstractmethod
    def next_pointer(self) -> Any:
        """
        The pointer that will be used to request the next page of Box objects.

        For limit-offset based paging, this is an offset. For marker-based paging, this is a marker.

        The pointer only gets progressed upon successful page requests to Box.
        """
        raise NotImplementedError
