# coding: utf-8

from __future__ import unicode_literals
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetworkResponse


def test_user_url(mock_user):
    # pylint:disable=redefined-outer-name, protected-access
    assert mock_user.get_url() == '{0}/{1}/{2}'.format(API.BASE_API_URL, 'users', mock_user.object_id)


@pytest.fixture(scope='module')
def memberships_response():
    # pylint disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'group_membership', 'id': 101, 'user': {'type': 'user', 'id': 100}, 'group': {'type': 'group', 'id': 300}},
            {'type': 'group_membership', 'id': 202, 'user': {'type': 'user', 'id': 200}, 'group': {'type': 'group', 'id': 400}}
        ],
        'limit': 2,
        'total_count': 2,
        'offset': 0,
    }
    return mock_network_response


def test_get_group_memberships(
        mock_user,
        mock_box_session,
        memberships_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = memberships_response
    memberships = mock_user.get_group_memberships()
    for membership, expected_id in zip(memberships, [101, 202]):
        assert membership.object_id == expected_id
        # pylint:disable=protected-access
        assert membership._session == mock_box_session
