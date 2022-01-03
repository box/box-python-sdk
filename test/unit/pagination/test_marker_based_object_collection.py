# coding: utf-8

import json
from mock import Mock, PropertyMock, ANY
import pytest

from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.pagination.marker_based_object_collection import MarkerBasedObjectCollection
from boxsdk.session.box_response import BoxResponse
from boxsdk.session.session import Session
from .box_object_collection_test_base import BoxObjectCollectionTestBase


class TestMarkerBasedObjectCollection(BoxObjectCollectionTestBase):
    """
    In order to conveniently mimic marker based paging for the purposes of this test, the markers ('next_marker' in
    the response) returned by the mock_session object is always going to be of the convention: "marker_i", where
    i is the starting 0-index based offset of the element.
    """

    NO_NEXT_MARKER = object()

    @staticmethod
    @pytest.fixture(params=['', None, NO_NEXT_MARKER])
    def next_marker_value_for_last_page(request):
        return request.param

    @pytest.fixture()
    def mock_items_response(self, entries, next_marker_value_for_last_page):
        """Baseclass override."""
        # pylint:disable=redefined-outer-name,arguments-differ
        def get_response(limit, marker):
            mock_box_response = Mock(BoxResponse)
            mock_network_response = Mock(DefaultNetworkResponse)
            mock_box_response.network_response = mock_network_response

            mock_json = {}
            # The marker string should be of format: "marker_i", where i is the offset. Parse that out.
            # If the marker is None, then begin paging from the start of the entries.
            offset = 0
            if marker is not None:
                offset = int(marker.split('_')[1])
            mock_json['entries'] = entries[offset:limit + offset]

            # A next_marker is only returned if there are more pages left.
            if (offset + limit) < len(entries):
                mock_json['next_marker'] = f'marker_{offset + limit}'
            elif next_marker_value_for_last_page is not self.NO_NEXT_MARKER:
                mock_json['next_marker'] = next_marker_value_for_last_page

            mock_box_response.json.return_value = mock_json
            mock_box_response.content = json.dumps(mock_json).encode()
            mock_box_response.status_code = 200
            mock_box_response.ok = True
            return mock_box_response
        return get_response

    @pytest.fixture()
    def mock_session(self, translator, mock_items_response):
        """Baseclass override."""
        mock_box_session = Mock(Session)
        type(mock_box_session).translator = PropertyMock(return_value=translator)

        def mock_items_side_effect(_, params):
            limit = params['limit']
            marker = params.get('marker', None)
            return mock_items_response(limit, marker)

        mock_box_session.get.side_effect = mock_items_side_effect
        return mock_box_session

    def _object_collection_instance(  # pylint:disable=arguments-differ
            self,
            session,
            limit,
            return_full_pages=False,
            starting_pointer=None,
            supports_limit_offset_paging=False
    ):
        """Baseclass override."""
        return MarkerBasedObjectCollection(
            session,
            '/some/endpoint',
            limit=limit,
            return_full_pages=return_full_pages,
            marker=starting_pointer,
            supports_limit_offset_paging=supports_limit_offset_paging,
        )

    @pytest.mark.parametrize('return_full_pages', (True, False))
    def test_object_collection_sets_next_pointer_correctly(self, mock_session, return_full_pages):
        object_collection = self._object_collection_instance(mock_session, limit=5, return_full_pages=return_full_pages)
        assert object_collection.next_pointer() is None
        object_collection.next()
        assert object_collection.next_pointer() == 'marker_5'

    @pytest.mark.parametrize('supports_limit_offset_paging', (True, False))
    def test_object_collection_specifies_marker_param(self, mock_session, supports_limit_offset_paging):
        object_collection = self._object_collection_instance(
            mock_session,
            limit=100,
            supports_limit_offset_paging=supports_limit_offset_paging
        )
        object_collection.next()

        # Assert
        expected_params = {'limit': 100}
        if supports_limit_offset_paging:
            expected_params['useMarker'] = True
        mock_session.get.assert_called_with(ANY, params=expected_params)
