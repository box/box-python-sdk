# coding: utf-8

import json
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.email_alias import EmailAlias
from boxsdk.object.folder import Folder
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment
from boxsdk.network.default_network import DefaultNetworkResponse


def test_user_url(mock_user):
    # pylint:disable=redefined-outer-name, protected-access
    assert mock_user.get_url() == f'{API.BASE_API_URL}/users/{mock_user.object_id}'


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


@pytest.fixture()
def test_email_alias(mock_box_session):
    return EmailAlias(
        session=mock_box_session,
        object_id='test_alias_id',
    )


def test_update(mock_user, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    user_id = mock_user.object_id
    expected_url = mock_box_session.get_url('users', user_id)
    user = {
        'type': 'user',
        'name': 'Test User',
        'id': 1234,
    }
    data = {
        'name': 'New User',
    }
    mock_box_session.put.return_value.json.return_value = user
    new_user = mock_user.update_info(data=data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert new_user.id == user['id']
    assert new_user.type == user['type']
    assert new_user.name == user['name']


def test_delete(mock_user, mock_box_session):
    user_id = mock_user.object_id
    expected_url = mock_box_session.get_url('users', user_id)
    expected_params = {
        'notify': True,
        'force': False,
    }
    mock_user.delete()
    mock_box_session.delete.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params=expected_params,
        headers=None,
    )


def test_get_email_aliases(mock_user, mock_box_session):
    # pylint:disable=redefined-outer-name
    alias1_json = {
        'type': 'email_alias',
        'id': '12345',
        'email': 'foo@example.com',
    }
    alias2_json = {
        'type': 'email_alias',
        'id': '67890',
        'email': 'bar@example.com',
    }
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 2,
        'entries': [alias1_json, alias2_json],
    }
    aliases = mock_user.get_email_aliases()
    for alias, alias_json in zip(aliases, [alias1_json, alias2_json]):
        assert alias.object_id == alias_json['id']
        # pylint:disable=protected-access
        assert alias._session == mock_box_session
        assert alias.email == alias_json['email']


def test_add_email_alias_returns_the_correct_email_alias_object(mock_user, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_email_alias = 'test@example.com'
    expected_url = f'{API.BASE_API_URL}/users/{mock_user.object_id}/email_aliases'
    expected_body = json.dumps({
        'email': test_email_alias,
    })
    mock_box_session.post.return_value.json.return_value = {
        'type': 'email_alias',
        'id': '1234',
        'email': test_email_alias,
    }
    new_email_alias = mock_user.add_email_alias(test_email_alias)
    mock_box_session.post.assert_called_once_with(expected_url, data=expected_body)
    assert isinstance(new_email_alias, EmailAlias)
    assert new_email_alias._session == mock_box_session  # pylint: disable=protected-access
    assert new_email_alias.object_id == '1234'


def test_remove_email_alias(mock_user, mock_box_session, test_email_alias):
    expected_url = f'{API.BASE_API_URL}/users/{mock_user.object_id}/email_aliases/{test_email_alias.object_id}'
    mock_box_session.delete.return_value.ok = True

    result = mock_user.remove_email_alias(test_email_alias)

    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False)
    assert result is True


@pytest.mark.parametrize('notify,fields,expected_params', [
    (None, None, {}),
    (True, None, {'notify': True}),
    (False, None, {'notify': False}),
    (None, ['type', 'id', 'name'], {'fields': 'type,id,name'}),
    (False, ['type', 'id'], {'notify': False, 'fields': 'type,id'}),
])
def test_transfer_content(mock_user, mock_box_session, notify, fields, expected_params):
    # pylint:disable=redefined-outer-name
    expected_url = f"{API.BASE_API_URL}/users/{mock_user.object_id}/folders/0"
    expected_body = json.dumps({
        'owned_by': {
            'id': mock_user.object_id
        },
    })
    move_items_response = {
        'type': 'folder',
        'id': '12345',
        'name': 'That Other User\'s Content',
    }
    mock_box_session.put.return_value.json.return_value = move_items_response
    moved_item = mock_user.transfer_content(mock_user, notify=notify, fields=fields)
    mock_box_session.put.assert_called_once_with(expected_url, data=expected_body, params=expected_params)
    assert isinstance(moved_item, Folder)
    assert moved_item.id == move_items_response['id']
    assert moved_item.name == move_items_response['name']
    assert moved_item._session == mock_box_session  # pylint:disable=protected-access


def test_get_group_memberships(
        mock_user,
        mock_box_session,
        memberships_response,
):
    # pylint:disable=redefined-outer-name
    expected_url = f'{API.BASE_API_URL}/users/{mock_user.object_id}/memberships'
    mock_box_session.get.return_value = memberships_response
    memberships = mock_user.get_group_memberships()
    for membership, expected_id in zip(memberships, [101, 202]):
        assert membership.object_id == expected_id
        # pylint:disable=protected-access
        assert membership._session == mock_box_session
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': None})


def test_get_user_avatar(mock_user, mock_box_session, mock_content_response):
    expected_url = mock_user.get_url('avatar')
    mock_box_session.get.return_value = mock_content_response
    avatar_content = mock_user.get_avatar()
    assert avatar_content == mock_content_response.content
    mock_box_session.get.assert_called_once_with(
        expected_url,
        expect_json_response=False,
    )
