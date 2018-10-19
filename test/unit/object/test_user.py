# coding: utf-8

from __future__ import unicode_literals

import json
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.email_alias import EmailAlias
from boxsdk.object.folder import Folder
from boxsdk.network.default_network import DefaultNetworkResponse


def test_user_url(mock_user):
    # pylint:disable=redefined-outer-name, protected-access
    assert mock_user.get_url() == '{0}/{1}/{2}'.format(API.BASE_API_URL, 'users', mock_user.object_id)


@pytest.fixture(scope='module')
def alias_id_1():
    return 101


@pytest.fixture(scope='module')
def alias_id_2():
    return 202


@pytest.fixture(scope='module')
def alias_response(alias_id_1, alias_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'email_alias', 'id': alias_id_1},
            {'type': 'email_alias', 'id': alias_id_2},
        ]
    }
    return mock_network_response


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


@pytest.fixture(scope='module')
def add_email_alias_response():
    #pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': 'email_alias',
        'id': '1234',
    }
    return mock_network_response


@pytest.fixture(scope='module')
def move_items_response():
    #pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': 'folder',
        'id': '1234',
    }
    return mock_network_response


def test_update(mock_user, mock_box_session):
    #pylint:disable=redefined-outer-name, protected-access
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
    new_user = mock_user.update_info(data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert new_user.id == user['id']
    assert new_user.type == user['type']
    assert new_user.name == user['name']


def test_delete(mock_user, mock_box_session):
    user_id = mock_user.object_id
    expected_url = mock_box_session.get_url('users', user_id)
    mock_user.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})


def test_email_aliases(mock_user, mock_box_session, alias_response, alias_id_1, alias_id_2):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = alias_response
    aliases = mock_user.email_aliases()
    for alias, expected_id in zip(aliases, [alias_id_1, alias_id_2]):
        assert alias.object_id == expected_id
        # pylint:disable=protected-access
        assert alias._session == mock_box_session


def test_add_email_alias_returns_the_correct_email_alias_object(mock_user, mock_box_session, add_email_alias_response):
    # pylint:disable=redefined-outer-name
    test_email_alias = 'test@example.com'
    value = json.dumps({
        'email': test_email_alias,
    })
    mock_box_session.post.return_value = add_email_alias_response
    new_email_alias = mock_user.add_email_alias(test_email_alias)
    assert len(mock_box_session.post.call_args_list) == 1
    assert mock_box_session.post.call_args[0] == ("{0}/users/{1}/email_aliases".format(API.BASE_API_URL, mock_user.object_id),)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_email_alias, EmailAlias)


def test_move_users_owned_items(mock_user, mock_box_session, move_items_response):
    # pylint:disable=redefined-outer-name
    value = json.dumps({
        'owned_by': {
            'id': mock_user.object_id
        },
    })
    mock_box_session.put.return_value = move_items_response
    moved_item = mock_user.move_owned_items(mock_user.object_id)
    assert len(mock_box_session.put.call_args_list) == 1
    assert mock_box_session.put.call_args[0] == ("{0}/users/fake-user-100/folders/0".format(API.BASE_API_URL),)
    assert mock_box_session.put.call_args[1] == {'data': value}
    assert isinstance(moved_item, Folder)


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
