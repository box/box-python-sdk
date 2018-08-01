# coding: utf-8

from __future__ import unicode_literals
import json

from mock import Mock
import pytest
from six import text_type

# pylint:disable=redefined-builtin
# pylint:disable=import-error
from six.moves import zip
# pylint:enable=redefined-builtin
# pylint:enable=import-error

from boxsdk.auth.oauth2 import OAuth2
from boxsdk.client import Client, DeveloperTokenClient, DevelopmentClient, LoggingClient
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.events import Events
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.object.group import Group
from boxsdk.object.user import User
from boxsdk.object.group_membership import GroupMembership
from boxsdk.object.retention_policy import RetentionPolicy
from boxsdk.object.storage_policy import StoragePolicy
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment
from boxsdk.object.webhook import Webhook


@pytest.fixture
def developer_token_input(monkeypatch):
    monkeypatch.setattr('boxsdk.auth.developer_token_auth.input', lambda prompt: 'developer_token')


@pytest.fixture(params=[Client, DeveloperTokenClient, DevelopmentClient, LoggingClient])
def mock_client(mock_box_session, developer_token_input, request):
    # pylint:disable=redefined-outer-name, unused-argument
    mock_oauth = Mock(OAuth2)
    client = request.param(mock_oauth)
    # pylint:disable=protected-access
    client._session = mock_box_session
    return client


@pytest.fixture(scope='module')
def user_id_1():
    return 1


@pytest.fixture(scope='module')
def user_id_2():
    return 1023


@pytest.fixture(scope='module')
def file_id():
    return 100


@pytest.fixture(scope='module')
def folder_id():
    return '1022'


@pytest.fixture(scope='module')
def webhook_id_1():
    return 101


@pytest.fixture(scope='module')
def webhook_id_2():
    return 202


@pytest.fixture(scope='module')
def webhooks_response(webhook_id_1, webhook_id_2):
    # pylint disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'webhook', 'id': webhook_id_1},
            {'type': 'webhook', 'id': webhook_id_2}
        ],
        'limit': 5,
    }
    return mock_network_response


@pytest.fixture(scope='module')
def create_webhook_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': 'webhook',
        'id': 1234
    }
    return mock_network_response


@pytest.fixture(scope='module')
def users_response(user_id_1, user_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {'entries': [
        {'type': 'user', 'id': user_id_1}, {'type': 'user', 'id': user_id_2}
    ]}
    return mock_network_response


@pytest.fixture(scope='module')
def user_response(user_id_1):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {'type': 'user', 'id': user_id_1}
    return mock_network_response


@pytest.fixture(scope='module')
def group_id_1():
    return 101


@pytest.fixture(scope='module')
def group_id_2():
    return 202


@pytest.fixture(scope='module')
def groups_response(group_id_1, group_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {'entries': [
        {'type': 'group', 'id': group_id_1, 'name': text_type(group_id_1)},
        {'type': 'group', 'id': group_id_2, 'name': text_type(group_id_2)},
    ]}
    return mock_network_response


@pytest.fixture(scope='module')
def create_group_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': 'group',
        'id': 1234,
        'name': 'test_group_name',
    }
    return mock_network_response


@pytest.fixture(scope='module')
def create_user_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': 'user',
        'id': 1234,
        'name': 'Ned Stark',
    }
    return mock_network_response


@pytest.fixture(scope='module', params=('file', 'folder'))
def shared_item_response(request):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': request.param,
        'id': 1234,
        'name': 'shared_item',
    }
    return mock_network_response


@pytest.fixture(scope='module')
def search_response(file_id, folder_id):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {'entries': [
        {'type': 'file', 'id': file_id}, {'type': 'folder', 'id': folder_id}
    ]}
    return mock_network_response


@pytest.mark.parametrize('test_class, factory_method_name', [
    (Folder, 'folder'),
    (File, 'file'),
    (User, 'user'),
    (Group, 'group'),
    (GroupMembership, 'group_membership'),
])
def test_factory_returns_the_correct_object(mock_client, test_class, factory_method_name):
    """ Tests the various id-only factory methods in the Client class """
    # pylint:disable=redefined-outer-name
    fake_id = 'fake_id'

    factory_method = getattr(mock_client, factory_method_name)

    obj = factory_method(fake_id)

    assert isinstance(obj, test_class)
    assert obj.object_id == fake_id


@pytest.fixture(scope='module', params=(None, 'user1'))
def users_filter_term(request):
    return request.param


@pytest.fixture(scope='module', params=(0, 10))
def users_offset(request):
    return request.param


@pytest.fixture(scope='module', params=(0, 10))
def users_limit(request):
    return request.param


def test_users_return_the_correct_user_objects(
        mock_client,
        mock_box_session,
        users_response,
        user_id_1,
        user_id_2,
        users_filter_term,
        users_offset,
        users_limit,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = users_response
    users = mock_client.users(users_limit, users_offset, users_filter_term)
    expected_params = {'offset': users_offset}
    if users_limit is not None:
        expected_params['limit'] = users_limit
    if users_filter_term is not None:
        expected_params['filter_term'] = users_filter_term
    mock_box_session.get.assert_called_once_with('{0}/users'.format(API.BASE_API_URL), params=expected_params)
    assert users[0].object_id == user_id_1
    assert users[1].object_id == user_id_2


def test_search_instantiates_search_and_calls_search(
        mock_client,
        mock_box_session,
        search_response,
        file_id,
        folder_id,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = search_response
    search_term = 'lolcatz'
    search_result = mock_client.search(
        search_term,
        10,
        0,
        ancestor_folders=[Folder(mock_box_session, folder_id)],
        file_extensions=['.jpg'],
    )
    assert search_result[0].object_id == file_id
    assert search_result[1].object_id == folder_id


def test_events_returns_event_object(mock_client):
    # pylint:disable=redefined-outer-name
    assert isinstance(mock_client.events(), Events)


def test_groups_return_the_correct_group_objects(
        mock_client,
        mock_box_session,
        groups_response,
        group_id_1,
        group_id_2,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = groups_response
    groups = mock_client.groups()
    for group, expected_id in zip(groups, [group_id_1, group_id_2]):
        assert group.object_id == expected_id
        assert group.name == str(expected_id)
        # pylint:disable=protected-access
        assert group._session == mock_box_session


def test_create_group_returns_the_correct_group_object(mock_client, mock_box_session, create_group_response):
    # pylint:disable=redefined-outer-name
    test_group_name = 'test_group_name'
    value = json.dumps({'name': test_group_name})
    mock_box_session.post.return_value = create_group_response
    new_group = mock_client.create_group(name=test_group_name)

    assert len(mock_box_session.post.call_args_list) == 1

    assert mock_box_session.post.call_args[0] == ("{0}/groups".format(API.BASE_API_URL),)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_group, Group)
    assert new_group.object_id == 1234
    assert new_group.name == test_group_name


@pytest.mark.parametrize('password', (None, 'p4ssw0rd'))
def test_get_shared_item_returns_the_correct_item(mock_client, mock_box_session, shared_item_response, password):
    # pylint:disable=redefined-outer-name
    shared_link = 'https://cloud.box.com/s/661wcw2iz6q5r7v5xxkm'
    mock_box_session.request.return_value = shared_item_response
    item = mock_client.get_shared_item(shared_link, password)
    assert item.type == shared_item_response.json()['type']
    mock_box_session.request.assert_called_once_with(
        'GET',
        '{0}/shared_items'.format(API.BASE_API_URL),
        headers={
            'BoxApi': 'shared_link={0}{1}'.format(
                shared_link, '&shared_link_password={0}'.format(password) if password is not None else ''
            ),
        },
    )


@pytest.mark.parametrize('test_method', [
    'get',
    'post',
    'put',
    'delete',
    'options',
])
def test_make_request_passes_request_on_to_session(mock_client, mock_box_session, test_method):
    # pylint:disable=redefined-outer-name
    mock_client.make_request(test_method, 'url')
    assert mock_box_session.request.call_args[0] == (test_method, 'url')


def test_create_app_user_returns_the_correct_user_object(mock_client, mock_box_session, create_user_response):
    # pylint:disable=redefined-outer-name
    test_user_name = 'Ned Stark'
    value = json.dumps({'name': test_user_name, 'is_platform_access_only': True})
    mock_box_session.post.return_value = create_user_response
    new_user = mock_client.create_user(name=test_user_name)

    assert len(mock_box_session.post.call_args_list) == 1

    assert mock_box_session.post.call_args[0] == ("{0}/users".format(API.BASE_API_URL),)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_user, User)
    assert new_user.object_id == 1234
    assert new_user.name == test_user_name


def test_create_enterprise_user_returns_the_correct_user_object(mock_client, mock_box_session, create_user_response):
    # pylint:disable=redefined-outer-name
    test_user_name = 'Ned Stark'
    test_user_login = 'eddard@box.com'
    value = json.dumps({'name': test_user_name, 'login': test_user_login})
    mock_box_session.post.return_value = create_user_response
    new_user = mock_client.create_user(name=test_user_name, login=test_user_login)

    assert len(mock_box_session.post.call_args_list) == 1

    assert mock_box_session.post.call_args[0] == ("{0}/users".format(API.BASE_API_URL),)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_user, User)
    assert new_user.object_id == 1234
    assert new_user.name == test_user_name


def test_create_webhook_returns_the_correct_policy_object(mock_client, mock_box_session, create_webhook_response):
    # pylint:disable=redefined-outer-name
    expected_body = {
        'target': {
            'type': 'file',
            'id': 42,
        },
        'triggers': ['FILE.DOWNLOADED'],
        'address': 'https://test.com',
    }
    value = json.dumps(expected_body)
    mock_box_session.post.return_value = create_webhook_response
    new_webhook = mock_client.create_webhook(42, 'file', ['FILE.DOWNLOADED'], 'https://test.com')
    assert len(mock_box_session.post.call_args_list) == 1
    assert mock_box_session.post.call_args[0] == ("{0}/webhooks".format(API.BASE_API_URL),)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_webhook, Webhook)


def test_get_assignments(
        mock_client,
        mock_box_session,
        webhooks_response,
        webhook_id_1,
        webhook_id_2,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = webhooks_response
    webhooks = mock_client.webhooks()
    for webhook, expected_id in zip(webhooks, [webhook_id_1, webhook_id_2]):
        assert webhook.object_id == expected_id
        # pylint:disable=protected-access
        assert webhook._session == mock_box_session


def test_get_storage_policies(mock_client, mock_box_session):
    expected_url = mock_box_session.get_url('storage_policies')
    mock_policy = {
        'type': 'storage_policy',
        'id': '12345',
        'name': 'Test Storage Policy'
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_policy]
    }

    policies = mock_client.storage_policies()
    policy = policies.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(policy, StoragePolicy)
    assert policy.id == mock_policy['id']
    assert policy.name == mock_policy['name']


def test_get_storage_policy_assignments(mock_client, mock_box_session):
    resolved_for_type = 'user'
    resolved_for_id = '1234'
    expected_url = mock_box_session.get_url('storage_policy_assignments')
    mock_assignment = {
        'type': 'storage_policy_assignment',
        'id': '12345',
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_assignment]
    }
    expected_params = {
        'limit': 100,
        'resolved_for_type': resolved_for_type,
        'resolved_for_id': resolved_for_id,
    }

    assignments = mock_client.storage_policy_assignments(resolved_for_type, resolved_for_id)
    assignment = assignments.next()
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert isinstance(assignment, StoragePolicyAssignment)
    assert assignment.id == mock_assignment['id']
    assert assignment.type == mock_assignment['type']


def test_create_retention_policy(mock_client, mock_box_session):
    policy_name = 'Test Retention Policy'
    policy_type = 'indefinite'
    disposition_action = 'remove_retention'
    expected_url = mock_box_session.get_url('retention_policies')
    expected_data = {
        'policy_name': policy_name,
        'policy_type': policy_type,
        'disposition_action': disposition_action,
        'can_owner_extend_retention': False,
        'are_owners_notified': False,
    }
    mock_policy = {
        'type': 'retention_policy',
        'id': '1234',
        'policy_name': policy_name,
    }
    mock_box_session.post.return_value.json.return_value = mock_policy
    policy = mock_client.create_retention_policy(policy_name, policy_type, disposition_action)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert policy.id == mock_policy['id']
    assert policy.type == mock_policy['type']


def test_get_retention_policies(mock_client, mock_box_session):
    expected_url = mock_box_session.get_url('retention_policies')
    mock_policy = {
        'type': 'retention_policy',
        'id': '12345',
        'name': 'Test Retention Policy',
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_policy],
        'next_marker': 'testMarker',
    }
    policies = mock_client.retention_policies()
    policy = policies.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'policy_name': None, 'policy_type': None, 'created_by_user_id': None})
    assert isinstance(policy, RetentionPolicy)
    assert policy.id == mock_policy['id']
    assert policy.name == mock_policy['name']
