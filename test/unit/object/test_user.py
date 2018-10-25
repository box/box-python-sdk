# coding: utf-8

from __future__ import unicode_literals
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment
from boxsdk.network.default_network import DefaultNetworkResponse


def test_user_url(mock_user):
    # pylint:disable=redefined-outer-name, protected-access
    assert mock_user.get_url() == '{0}/{1}/{2}'.format(API.BASE_API_URL, 'users', mock_user.object_id)


def test_get_storage_policy_assignments(test_storage_policy_assignment, mock_user, mock_box_session):
    expected_url = mock_box_session.get_url('storage_policy_assignments')
    mock_assignment = {
        'type': test_storage_policy_assignment.object_type,
        'id': test_storage_policy_assignment.object_id,
        'assigned_to': {
            'type': mock_user.object_type,
            'id': mock_user.object_id,
        },
    }
    mock_box_session.get.return_value.json.return_value = {
        'next_marker': None,
        'limit': 1,
        'entries': [mock_assignment],
    }
    expected_params = {
        'resolved_for_type': mock_user.object_type,
        'resolved_for_id': mock_user.object_id,
    }
    assignment = mock_user.get_storage_policy_assignment()
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert isinstance(assignment, StoragePolicyAssignment)
    assert assignment.id == mock_assignment['id']
    assert assignment.type == mock_assignment['type']


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
    expected_url = '{0}/users/{1}/memberships'.format(API.BASE_API_URL, mock_user.object_id)
    mock_box_session.get.return_value = memberships_response
    memberships = mock_user.get_group_memberships()
    for membership, expected_id in zip(memberships, [101, 202]):
        assert membership.object_id == expected_id
        # pylint:disable=protected-access
        assert membership._session == mock_box_session
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': None})
