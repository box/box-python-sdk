# coding: utf-8

import json

from mock import Mock, PropertyMock
import pytest

from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from boxsdk.session.box_response import BoxResponse
from boxsdk.session.session import Session
from .box_object_collection_test_base import BoxObjectCollectionTestBase


class TestLimitOffsetBasedObjectCollection(BoxObjectCollectionTestBase):
    DEFAULT_LIMIT = 100

    @pytest.fixture()
    def mock_items_response(self, entries):
        """Baseclass override."""
        # pylint:disable=redefined-outer-name
        def get_response(limit, offset):
            mock_box_response = Mock(BoxResponse)
            mock_network_response = Mock(DefaultNetworkResponse)
            mock_box_response.network_response = mock_network_response
            mock_box_response.json.return_value = mock_json = {
                'entries': entries[offset:limit + offset],
                'total_count': len(entries),
                'limit': limit,
            }
            mock_box_response.content = json.dumps(mock_json).encode()
            mock_box_response.status_code = 200
            mock_box_response.ok = True
            return mock_box_response
        return get_response

    @pytest.fixture()
    def mock_session(self, translator, mock_items_response):
        """Baseclass override."""
        mock_box_session = Mock(Session)
        type(mock_box_session).translator = PropertyMock(
            return_value=translator
        )

        def mock_items_side_effect(_, params):
            limit = min(params.get('limit', self.DEFAULT_LIMIT), self.DEFAULT_LIMIT)
            offset = params.get('offset', 0)
            return mock_items_response(limit, offset)

        mock_box_session.get.side_effect = mock_items_side_effect
        return mock_box_session

    @pytest.fixture()
    def mock_session_with_bogus_limit(self, mock_session, mock_items_response):
        """Baseclass override."""
        # pylint:disable=no-self-use

        def mock_items_side_effect(_, params):
            limit = 0
            offset = params.get('offset', 0)
            return mock_items_response(limit, offset)

        mock_session.get.side_effect = mock_items_side_effect
        return mock_session

    def _object_collection_instance(self, session, limit=None, return_full_pages=False, starting_pointer=None):
        """Baseclass override."""
        if starting_pointer is None:
            starting_pointer = 0
        return LimitOffsetBasedObjectCollection(
            session,
            '/some/endpoint',
            limit=limit,
            return_full_pages=return_full_pages,
            offset=starting_pointer,
        )

    @pytest.mark.parametrize('return_full_pages', (True, False))
    def test_object_collection_sets_next_pointer_correctly(self, mock_session, return_full_pages):
        page_size = 10
        object_collection = LimitOffsetBasedObjectCollection(
            mock_session,
            '/some/endpoint',
            limit=page_size,
            return_full_pages=return_full_pages,
        )

        assert object_collection.next_pointer() == 0
        object_collection.next()
        assert object_collection.next_pointer() == page_size

        # Iterate to the last page, which doesn't return a full page.
        list(object_collection)
        assert object_collection.next_pointer() == self.NUM_ENTRIES

    def test_object_collection_raises_stop_iteration_when_starting_offset_is_too_far(self, mock_session, entries):
        """
        If the specified initial offset for the object collection is higher than the total number of items,
        then the first call to next() on the object collection should raise a StopIteration.
        """
        starting_offset = len(entries) + 10
        object_collection = self._object_collection_instance(
            mock_session,
            limit=5,
            return_full_pages=False,
            starting_pointer=starting_offset
        )
        with pytest.raises(StopIteration):
            object_collection.next()

    def test_object_collection_sets_limit_to_returned_value_if_originally_none(self, mock_session):
        # No limit specified
        object_collection = self._object_collection_instance(mock_session)
        object_collection.next()
        assert object_collection._limit == self.DEFAULT_LIMIT   # pylint:disable=protected-access

    def test_object_collection_sets_limit_to_returned_value_if_originally_too_high(self, mock_session):
        object_collection = self._object_collection_instance(mock_session, limit=(1 + self.DEFAULT_LIMIT))
        object_collection.next()
        assert object_collection._limit == self.DEFAULT_LIMIT   # pylint:disable=protected-access

    def test_box_returning_bogus_limit_raises_runtime_error(self, mock_session_with_bogus_limit, entries):
        """
        Confirm that the SDK raises a RuntimeError is box.com happens to return a bogus `limit` in the response
        """
        starting_offset = len(entries) + 10
        object_collection = self._object_collection_instance(
            mock_session_with_bogus_limit,
            limit=5,
            return_full_pages=False,
            starting_pointer=starting_offset
        )
        with pytest.raises(RuntimeError):
            object_collection.next()
