# coding: utf-8

from itertools import chain, islice, repeat, count
import json
from operator import sub

from mock import Mock
import pytest

from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.group_membership import GroupMembership
from boxsdk.object.user import User
from boxsdk.config import API
from boxsdk.session.box_response import BoxResponse


@pytest.fixture(scope='module')
def delete_group_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_delete_group_return_the_correct_response(
        mock_group,
        mock_box_session,
        delete_group_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_group_response
    response = mock_group.delete()

    # pylint:disable=protected-access
    expected_url = mock_group.get_url()
    # pylint:enable=protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)

    assert response is True


@pytest.mark.parametrize('role', ['member', 'admin'])
def test_add_member(test_group, mock_box_session, mock_add_member_response, mock_user, role):
    expected_url = f'{API.BASE_API_URL}/group_memberships'
    mock_box_session.post.return_value = mock_add_member_response
    new_group_membership = test_group.add_member(mock_user, role, configurable_permissions={'can_run_reports': True})
    data = json.dumps({
        'user': {'id': mock_user.object_id},
        'group': {'id': test_group.object_id},
        'role': role,
        'configurable_permissions': {'can_run_reports': True}
    })
    mock_box_session.post.assert_called_once_with(expected_url, data=data)
    assert isinstance(new_group_membership, GroupMembership)


def test_add_member_default_permission(test_group, mock_box_session, mock_add_member_response, mock_user):
    expected_url = f'{API.BASE_API_URL}/group_memberships'
    mock_box_session.post.return_value = mock_add_member_response
    new_group_membership = test_group.add_member(mock_user, 'member')
    data = json.dumps({
        'user': {'id': mock_user.object_id},
        'group': {'id': test_group.object_id},
        'role': 'member',
    })
    mock_box_session.post.assert_called_once_with(expected_url, data=data)
    assert isinstance(new_group_membership, GroupMembership)


def test_add_member_none_permission(test_group, mock_box_session, mock_add_member_response, mock_user):
    expected_url = f'{API.BASE_API_URL}/group_memberships'
    mock_box_session.post.return_value = mock_add_member_response
    new_group_membership = test_group.add_member(mock_user, 'member', configurable_permissions=None)
    data = json.dumps({
        'user': {'id': mock_user.object_id},
        'group': {'id': test_group.object_id},
        'role': 'member',
        'configurable_permissions': None
    })
    mock_box_session.post.assert_called_once_with(expected_url, data=data)
    assert isinstance(new_group_membership, GroupMembership)


@pytest.fixture()
def mock_membership_dict_stream():
    def gen_data(some_id):
        return {
            'type': 'group_membership',
            'id': f"membership_id_{some_id}",
            'role': 'member',
            'user': {'type': 'user', 'id': f"user_id_{some_id}"},
            'group': {'type': 'group', 'id': f"group_id_{some_id}"},
        }

    return map(gen_data, count())


@pytest.fixture()
def mock_membership_responses(mock_membership_dict_stream):
    """
    Returns a generator method that takes params: total, page_size.
    The generator generates a sequence of 'group membership' mock_box_responses each containing page_size
    items, until 'total' entries have been returned
    """
    # pylint:disable=redefined-outer-name
    def number_entries_per_response(total, page_size, hidden_in_batch):
        if not hidden_in_batch:
            hidden_in_batch = repeat(0)
        quotient, remainder = divmod(total, page_size)
        max_items_in_batch = chain(repeat(page_size, quotient), (remainder,))
        return map(sub, max_items_in_batch, hidden_in_batch)

    def take(iterable, number):
        return list(islice(iterable, number))

    def membership_responses(total, page_size, hidden_in_batch=None):
        offset = 0
        for number_entries in number_entries_per_response(total, page_size, hidden_in_batch):
            entries = take(mock_membership_dict_stream, number_entries)

            mock_box_response = Mock(BoxResponse)
            mock_network_response = Mock(DefaultNetworkResponse)
            mock_box_response.network_response = mock_network_response
            mock_box_response.json.return_value = {
                'entries': entries,
                'total_count': total,
                'offset': offset,
                'limit': page_size,
            }
            offset += page_size
            mock_box_response.status_code = 200
            mock_box_response.ok = True
            yield mock_box_response

    return membership_responses


@pytest.mark.parametrize('total, page_size', [
    (0, 6),
    (5, 6),
    (6, 6),
    (5, 4),
    (9, 4),
])
def test_get_memberships(test_group, mock_box_session, mock_membership_responses, total, page_size):
    # pylint:disable=redefined-outer-name
    # Each call the 'get' (the GET next page call) will return the next response
    mock_box_session.get.side_effect = mock_membership_responses(total, page_size)

    # Get all the members
    all_members = test_group.get_memberships()

    # Assert we got the expected number of membership instances
    count = 0
    for membership in all_members:
        count += 1
        assert isinstance(membership, GroupMembership)
    assert count == total


@pytest.mark.parametrize('hidden_in_batch', [
    (1, 0, 0),
    (0, 0, 1),
    (10, 10, 9),
    (10, 10, 10),
])
def test_get_memberships_with_hidden_results(test_group, mock_box_session, mock_membership_responses, hidden_in_batch):
    """
    This test verifies that the SDK properly deals with missing (aka hidden) data potentially present in a paged
    API. The API might indicate that the total_size is X, but in actuality the pages API could return less than X
    because the auth'd user might not have access to all X of the resources.
    """
    # pylint:disable=redefined-outer-name
    total = 30
    page_size = 10

    total_hidden = sum(hidden_in_batch)

    # Each call the 'get' (the GET next page call) will return the next response
    mock_box_session.get.side_effect = mock_membership_responses(total, page_size, hidden_in_batch=hidden_in_batch)

    # Get all the members
    all_members = test_group.get_memberships(limit=page_size, offset=0)

    # Assert we got the expected number of membership instances
    count = 0
    for membership in all_members:
        count += 1
        assert isinstance(membership, GroupMembership)
    assert count == total - total_hidden


def test_get_group_collaborations(test_group, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/groups/{test_group.object_id}/collaborations'
    mock_collaboration = {
        'type': 'collaboration',
        'id': '12345',
        'created_by': {
            'type': 'user',
            'id': '33333'
        }
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_collaboration],
        'offset': 0,
        'total_count': 1
    }
    collaborations = test_group.get_collaborations(fields=['type', 'id', 'created_by'])
    collaboration = collaborations.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': None, 'fields': 'type,id,created_by'})
    assert isinstance(collaboration, Collaboration)
    assert collaboration.id == mock_collaboration['id']
    assert collaboration.created_by['id'] == mock_collaboration['created_by']['id']


def test_base_api_json_object_returns_correctly(test_group_membership, mock_box_session):
    expected_data = {
        'type': 'group_membership',
        'id': '12345',
        'test': [
            {
                'user': {
                    'type': 'user'
                }
            },
            {
                'group': {
                    'type': 'group'
                }
            },
        ],
        'user': {
            'type': 'user',
            'id': '5678',
            'name': 'Test User',
            'login': 'test@example.com',
        },
        'group': {
            'type': 'group',
            'id': '54321',
            'name': 'Test'
        },
        'role': 'admin',
        'configurable_permissions': {
            'can_run_reports': False,
            'can_instant_login': True,
            'can_create_accounts': False,
            'can_edit_accounts': True,
        },
        'created_at': '2013-05-16T15:27:57-07:00',
        'modified_at': '2013-05-16T15:27:57-07:00',
    }
    mock_box_session.get.return_value.json.return_value = expected_data
    membership = test_group_membership.get()
    membership_response = membership.response_object
    assert isinstance(membership.user, User)
    assert isinstance(membership_response, dict)
    assert membership_response is not expected_data
    assert membership_response == expected_data
