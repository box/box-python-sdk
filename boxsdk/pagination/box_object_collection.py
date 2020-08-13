# coding: utf-8

from __future__ import unicode_literals

import sys
from abc import ABCMeta, abstractmethod

from six import add_metaclass

from boxsdk.pagination.page import Page

if sys.version_info >= (3, 3):
    from collections.abc import Iterator  # pylint:disable=no-name-in-module,import-error
else:
    from collections import Iterator  # pylint:disable=no-name-in-module,import-error


@add_metaclass(ABCMeta)
class BoxObjectCollection(Iterator):
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
            session,
            url,
            limit=None,
            fields=None,
            additional_params=None,
            return_full_pages=False,
    ):
        """
        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        :param url:
            The endpoint url to hit.
        :type url:
            `unicode`
        :param limit:
            The number of entries for each page to return. The default, as well as the upper limit of this value,
            differs by endpoint. See https://developer.box.com/en/reference. If limit is set to None, then the default
            limit (returned by Box in the response) is used.
        :type limit:
            `int` or None
        :param fields:
            List of fields to request. If None, will return the default fields for the object.
        :type fields:
            `Iterable` of `unicode` or None
        :param additional_params:
            Additional HTTP params to send in the request.
        :type additional_params:
            `dict` or None
        :param return_full_pages:
            If True, then the returned iterator for this collection will return full pages of Box objects on each
            call to next(). If False, the iterator will return a single Box object on each next() call.
        :type return_full_pages:
            `bool`
        """
        super(BoxObjectCollection, self).__init__()
        self._session = session
        self._url = url
        self._limit = limit
        self._fields = fields
        self._additional_params = additional_params
        self._return_full_pages = return_full_pages
        self._has_retrieved_all_items = False
        self._all_items = None

    def next(self):
        """
        Returns either a Page (a Sequence of BaseObjects) or a BaseObject depending on self._return_full_pages.

        Invoking this method may make an API call to Box. Any exceptions that can occur while making requests
        may be raised in this method.

        :rtype:
            :class:`Page` or :class:`BaseObject`
        """
        if self._all_items is None:
            self._all_items = self._items_generator()
        return next(self._all_items)

    __next__ = next

    def _items_generator(self):
        """
        :rtype:
            :class:`Page` or :class:`BaseObject`
        """
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

    def _load_next_page(self):
        """
        Request the next page of entries from Box. Raises any network-related exceptions, including BoxAPIException.
        Returns a parsed dictionary of the JSON response from Box

        :rtype:
            `dict`
        """
        params = {}
        if self._limit is not None:
            params['limit'] = self._limit
        if self._fields:
            params['fields'] = ','.join(self._fields)
        if self._additional_params:
            params.update(self._additional_params)
        params.update(self._next_page_pointer_params())
        box_response = self._session.get(self._url, params=params)
        return box_response.json()

    @abstractmethod
    def _update_pointer_to_next_page(self, response_object):
        """
        Update the internal pointer attribute of this class to what will be used to request the next page
        of Box objects.

        A "pointer" can either be a marker (for marker-based paging) or an offset (for limit-offset paging).

        :param response_object:
            The parsed HTTP response from Box after requesting more pages.
        :type response_object:
            `dict`
        """
        raise NotImplementedError

    @abstractmethod
    def _has_more_pages(self, response_object):
        """
        Are there more pages of entries to query Box for? This gets invoked after self._update_pointer_to_next_page().

        :param response_object:
            The parsed HTTP response from Box after requesting more pages.
        :type response_object:
            `dict`
        :rtype:
            `bool`
        """
        raise NotImplementedError

    @abstractmethod
    def _next_page_pointer_params(self):
        """
        The dict of HTTP params that specify which page of Box objects to retrieve.

        :rtype:
            `dict`
        """
        raise NotImplementedError

    @abstractmethod
    def next_pointer(self):
        """
        The pointer that will be used to request the next page of Box objects.

        For limit-offset based paging, this is an offset. For marker-based paging, this is a marker.

        The pointer only gets progressed upon successful page requests to Box.

        :rtype:
            varies
        """
        raise NotImplementedError
