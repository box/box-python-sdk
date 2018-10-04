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

from boxsdk.auth.oauth2 import OAuth2, TokenScope
from boxsdk.client import Client, DeveloperTokenClient, DevelopmentClient, LoggingClient
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.events import Events
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.object.group import Group
from boxsdk.object.user import User
from boxsdk.object.trash import Trash
from boxsdk.object.group_membership import GroupMembership
from boxsdk.object.retention_policy import RetentionPolicy
from boxsdk.object.file_version_retention import FileVersionRetention
from boxsdk.object.legal_hold_policy import LegalHoldPolicy
from boxsdk.object.webhook import Webhook
from boxsdk.pagination.marker_based_object_collection import MarkerBasedObjectCollection


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


@pytest.fixture()
def test_folder(mock_box_session, mock_object_id):
    return Folder(mock_box_session, mock_object_id)


@pytest.fixture()
def test_webhook(mock_box_session, mock_object_id):
    return Webhook(mock_box_session, mock_object_id)


@pytest.fixture(scope='function')
def mock_file_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'file', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture(scope='function')
def mock_folder_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'folder', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture(scope='module')
def marker_id():
    return 'marker_1'


@pytest.fixture(scope='module')
def users_response(user_id_1, user_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'user', 'id': user_id_1},
            {'type': 'user', 'id': user_id_2}
        ],
        'limit': 100,
        'offset': 0,
        'total_count': 2
    }
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


@pytest.fixture()
def mock_user(mock_box_session):
    user = User(mock_box_session, '12345')
    return user


@pytest.fixture()
def mock_user_list(mock_box_session):
    user_list = []
    first_user = User(mock_box_session, '33333')
    second_user = User(mock_box_session, '44444')
    user_list = [first_user, second_user]
    return user_list


@pytest.fixture()
def mock_file(mock_box_session):
    test_file = File(mock_box_session, '11111')
    return test_file


@pytest.fixture()
def mock_retention_policy(mock_box_session):
    retention_policy = RetentionPolicy(mock_box_session, '22222')
    return retention_policy


@pytest.fixture(scope='module')
def groups_response(group_id_1, group_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'group', 'id': group_id_1, 'name': text_type(group_id_1)},
            {'type': 'group', 'id': group_id_2, 'name': text_type(group_id_2)},
        ],
        'limit': 100,
        'offset': 0,
        'total_count': 2
    }
    return mock_network_response


@pytest.fixture(scope='module')
def legal_hold_policy_id_1():
    return 101


@pytest.fixture(scope='module')
def legal_hold_policy_id_2():
    return 202


@pytest.fixture(scope='module')
def legal_hold_policies_response(legal_hold_policy_id_1, legal_hold_policy_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'legal_hold_policy', 'id': legal_hold_policy_id_1, 'name': 'Test Policy 1'},
            {'type': 'legal_hold_policy', 'id': legal_hold_policy_id_2, 'name': 'Test Policy 2'},
        ],
        'limit': 5,
    }
    return mock_network_response


@pytest.fixture(scope='module')
def create_policy_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': 'legal_hold_policy',
        'id': 1234,
        'policy_name': 'Test Policy'
    }
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


@pytest.fixture(params=('file', 'folder'))
def test_item_and_response(mock_file, test_folder, mock_file_response, mock_folder_response, request):
    if request.param == 'file':
        return mock_file, mock_file_response
    return test_folder, mock_folder_response


@pytest.fixture()
def create_webhook_response(test_item_and_response, test_webhook):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': test_webhook.object_type,
        'id': test_webhook.object_id,
        'target': {
            'type': test_item.object_type,
            'id': test_item.object_id,
        },
        'created_at': '2016-05-09T17:41:27-07:00',
        'address': 'https://test.com',
        'triggers': [
            'FILE.UPLOADED',
            'FOLDER.CREATED',
        ],
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
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'file', 'id': file_id},
            {'type': 'folder', 'id': folder_id}
        ],
        'limit': 100,
        'offset': 0,
        'total_count': 2
    }
    return mock_network_response


@pytest.fixture(scope='module')
def recent_items_response(file_id):
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'recent_item', 'item': {'type': 'file', 'id': file_id}}
        ],
        'next_marker': None,
        'limit': 100,
    }
    return mock_network_response


@pytest.fixture(scope='module')
def device_pin_id_1():
    return 101


@pytest.fixture(scope='module')
def device_pin_id_2():
    return 202


@pytest.fixture(scope='module')
def device_pins_response(device_pin_id_1, device_pin_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'device_pinner', 'id': device_pin_id_1},
            {'type': 'device_pinner', 'id': device_pin_id_2},
        ],
        'limit': 2,
    }
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
    assert users.next().object_id == user_id_1
    assert users.next().object_id == user_id_2
    mock_box_session.get.assert_called_once_with('{0}/users'.format(API.BASE_API_URL), params=expected_params)


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
    assert search_result.next().object_id == file_id
    assert search_result.next().object_id == folder_id


def test_events_returns_event_object(mock_client):
    # pylint:disable=redefined-outer-name
    assert isinstance(mock_client.events(), Events)


def test_get_groups_return_the_correct_group_objects(
        mock_client,
        mock_box_session,
        groups_response,
        group_id_1,
        group_id_2,
):
    # pylint:disable=redefined-outer-name
    expected_url = '{0}/groups'.format(API.BASE_API_URL)
    mock_box_session.get.return_value = groups_response
    groups = mock_client.get_groups()
    for group, expected_id in zip(groups, [group_id_1, group_id_2]):
        assert group.object_id == expected_id
        assert group.name == str(expected_id)
        # pylint:disable=protected-access
        assert group._session == mock_box_session
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': None})


def test_create_group_returns_the_correct_group_object(mock_client, mock_box_session, create_group_response):
    # pylint:disable=redefined-outer-name
    expected_url = "{0}/groups".format(API.BASE_API_URL)
    test_group_name = 'test_group_name'
    value = json.dumps({
        'name': test_group_name,
        'provenance': 'Example',
        'external_sync_identifier': 'Example-User',
        'description': 'Description of group',
        'invitability_level': 'admins_and_members',
        'member_viewability_level': 'admins_only',
    })
    mock_box_session.post.return_value = create_group_response
    new_group = mock_client.create_group(
        name=test_group_name,
        provenance='Example',
        external_sync_identifier='Example-User',
        description='Description of group',
        invitability_level='admins_and_members',
        member_viewability_level='admins_only',
    )

    assert len(mock_box_session.post.call_args_list) == 1

    mock_box_session.post.assert_called_once_with(expected_url, data=value, params={})
    assert isinstance(new_group, Group)
    assert new_group.object_id == 1234
    assert new_group.name == test_group_name


def test_create_legal_hold_policy_returns_the_correct_policy_object(mock_client, mock_box_session, create_policy_response):
    # pylint:disable=redefined-outer-name
    test_policy_name = 'Test Policy'
    expected_body = {
        'policy_name': test_policy_name
    }
    value = json.dumps(expected_body)
    mock_box_session.post.return_value = create_policy_response
    new_policy = mock_client.create_legal_hold_policy(test_policy_name)
    assert len(mock_box_session.post.call_args_list) == 1
    assert mock_box_session.post.call_args[0] == ("{0}/legal_hold_policies".format(API.BASE_API_URL),)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_policy, LegalHoldPolicy)
    assert new_policy.policy_name == test_policy_name


def test_legal_hold_policies_return_the_correct_policy_objects(
        mock_client,
        mock_box_session,
        legal_hold_policies_response,
        legal_hold_policy_id_1,
        legal_hold_policy_id_2,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = legal_hold_policies_response
    policies = mock_client.get_legal_hold_policies()
    for policy, expected_id in zip(policies, [legal_hold_policy_id_1, legal_hold_policy_id_2]):
        assert policy.object_id == expected_id
        # pylint:disable=protected-access
        assert policy._session == mock_box_session


def test_trash_initializer(mock_client):
    trash = mock_client.trash()
    assert isinstance(trash, Trash)


def test_get_recent_items_returns_the_correct_items(mock_client, mock_box_session, recent_items_response, file_id):
    mock_box_session.get.return_value = recent_items_response
    recent_items = mock_client.get_recent_items()
    assert isinstance(recent_items, MarkerBasedObjectCollection)
    recent_item = recent_items.next()
    assert recent_item.item.object_id == file_id
    next_pointer = recent_items.next_pointer()
    assert next_pointer is None


def test_get_recent_items_sends_get_with_correct_params(mock_client, mock_box_session, recent_items_response, marker_id):
    limit = 50
    marker = marker_id
    fields = ['modified_at', 'name']
    expected_params = {
        'limit': limit,
        'marker': marker_id,
        'fields': ','.join(fields),
    }
    mock_box_session.get.return_value = recent_items_response
    object_collection = mock_client.get_recent_items(limit=limit, marker=marker, fields=fields)
    object_collection.next()
    mock_box_session.get.assert_called_once_with('{0}/recent_items'.format(API.BASE_API_URL), params=expected_params)


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


def test_webhook_initializer(mock_client):
    expected_id = '1234'
    webhook = mock_client.webhook(expected_id)
    assert isinstance(webhook, Webhook)
    assert webhook.object_id == expected_id


def test_create_webhook_returns_the_correct_policy_object(
        test_item_and_response,
        test_webhook,
        mock_client,
        mock_box_session,
        create_webhook_response,
):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = "{0}/webhooks".format(API.BASE_API_URL)
    expected_body = {
        'target': {
            'type': test_item.object_type,
            'id': test_item.object_id,
        },
        'triggers': ['FILE.UPLOADED', 'FOLDER.CREATED'],
        'address': 'https://test.com',
    }
    value = json.dumps(expected_body)
    mock_box_session.post.return_value = create_webhook_response
    new_webhook = mock_client.create_webhook(test_item, ['FILE.UPLOADED', 'FOLDER.CREATED'], 'https://test.com')
    mock_box_session.post.assert_called_once_with(
        expected_url,
        data=value,
    )
    assert isinstance(new_webhook, Webhook)
    assert new_webhook.id == test_webhook.object_id
    assert new_webhook.type == test_webhook.object_type
    assert new_webhook.target['type'] == test_item.object_type
    assert new_webhook.target['id'] == test_item.object_id
    assert new_webhook.triggers == ['FILE.UPLOADED', 'FOLDER.CREATED']
    assert new_webhook.address == 'https://test.com'


def test_get_webhooks(mock_client, mock_box_session):
    expected_url = "{0}/webhooks".format(API.BASE_API_URL)
    webhook_body = {
        'type': 'webhook',
        'id': '12345',
        'target': {
            'type': 'folder',
            'id': '11111',
        },
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [webhook_body],
    }
    webhooks = mock_client.get_webhooks()
    webhook = webhooks.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(webhook, Webhook)
    assert webhook.object_id == webhook_body['id']
    assert webhook.object_type == webhook_body['type']
    assert webhook.target['id'] == webhook_body['target']['id']
    assert webhook.target['type'] == webhook_body['target']['type']


def test_create_retention_policy(mock_client, mock_box_session, mock_user_list):
    policy_name = 'Test Retention Policy'
    policy_type = 'finite'
    disposition_action = 'remove_retention'
    expected_url = "{0}/retention_policies".format(API.BASE_API_URL)
    expected_data = {
        'policy_name': policy_name,
        'disposition_action': disposition_action,
        'policy_type': 'finite',
        'retention_length': 5,
        'can_owner_extend_retention': True,
        'are_owners_notified': False,
        'custom_notification_recipients': [
            {
                'type': mock_user_list[0].object_type,
                'id': mock_user_list[0].object_id,
            },
            {
                'type': mock_user_list[1].object_type,
                'id': mock_user_list[1].object_id,
            },
        ],
    }
    mock_policy = {
        'type': 'retention_policy',
        'id': '1234',
        'policy_name': policy_name,
        'policy_type': policy_type,
        'retention_length': 5,
        'disposition_action': disposition_action,
        'can_owner_extend_retention': False,
        'are_owners_notified': False,
        'custom_notification_recipients': [
            {
                'type': mock_user_list[0].object_type,
                'id': mock_user_list[0].object_id,
            },
            {
                'type': mock_user_list[1].object_type,
                'id': mock_user_list[1].object_id,
            },
        ],
    }
    mock_box_session.post.return_value.json.return_value = mock_policy
    policy = mock_client.create_retention_policy(
        policy_name=policy_name,
        disposition_action=disposition_action,
        retention_length=5,
        can_owner_extend_retention=True,
        are_owners_notified=False,
        custom_notification_recipients=mock_user_list
    )
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert policy.object_id == mock_policy['id']
    assert policy.object_type == mock_policy['type']
    assert policy.policy_name == mock_policy['policy_name']
    assert policy.disposition_action == mock_policy['disposition_action']
    assert policy.can_owner_extend_retention == mock_policy['can_owner_extend_retention']
    assert policy.are_owners_notified == mock_policy['are_owners_notified']
    assert isinstance(policy, RetentionPolicy)


def test_create_infinte_retention_policy(mock_client, mock_box_session):
    policy_name = 'Test Retention Policy'
    policy_type = 'indefinite'
    disposition_action = 'remove_retention'
    expected_url = "{0}/retention_policies".format(API.BASE_API_URL)
    expected_data = {
        'policy_name': policy_name,
        'disposition_action': disposition_action,
        'policy_type': policy_type,
        'can_owner_extend_retention': False,
        'are_owners_notified': False,
    }
    mock_policy = {
        'type': 'retention_policy',
        'id': '1234',
        'policy_name': policy_name,
        'policy_type': policy_type,
        'disposition_action': disposition_action,
        'can_owner_extend_retention': False,
        'are_owners_notified': False,
    }
    mock_box_session.post.return_value.json.return_value = mock_policy
    policy = mock_client.create_retention_policy(
        policy_name=policy_name,
        disposition_action=disposition_action,
        retention_length=float('inf'),
        can_owner_extend_retention=False,
        are_owners_notified=False
    )
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert policy.object_id == mock_policy['id']
    assert policy.object_type == mock_policy['type']
    assert policy.policy_name == mock_policy['policy_name']
    assert policy.disposition_action == mock_policy['disposition_action']
    assert policy.can_owner_extend_retention == mock_policy['can_owner_extend_retention']
    assert policy.are_owners_notified == mock_policy['are_owners_notified']
    assert isinstance(policy, RetentionPolicy)


def test_get_retention_policies(mock_client, mock_box_session, mock_user):
    expected_url = "{0}/retention_policies".format(API.BASE_API_URL)
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
    policies = mock_client.get_retention_policies(policy_name='Test Name', policy_type='finite', user=mock_user)
    policy = policies.next()
    params = {
        'policy_name': 'Test Name',
        'policy_type': 'finite',
        'created_by_user_id': '12345',
    }
    mock_box_session.get.assert_called_once_with(expected_url, params=params)
    assert isinstance(policy, RetentionPolicy)
    assert policy.id == mock_policy['id']
    assert policy.name == mock_policy['name']


def test_get_file_version_retentions(mock_client, mock_box_session, mock_file, mock_retention_policy):
    expected_url = "{0}/file_version_retentions".format(API.BASE_API_URL)
    mock_retention = {
        'type': 'file_version_retention',
        'id': '12345',
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_retention],
        'next_marker': 'testMarker',
    }
    retentions = mock_client.get_file_version_retentions(
        target_file=mock_file,
        policy=mock_retention_policy,
        disposition_action='remove_retention',
        disposition_before='2014-09-15T13:15:35-07:00',
        disposition_after='2014-09-20T13:15:35-07:00',
    )
    retention = retentions.next()
    params = {
        'file_id': '11111',
        'policy_id': '22222',
        'disposition_action': 'remove_retention',
        'disposition_before': '2014-09-15T13:15:35-07:00',
        'disposition_after': '2014-09-20T13:15:35-07:00',
    }
    mock_box_session.get.assert_called_once_with(expected_url, params=params)
    assert isinstance(retention, FileVersionRetention)
    assert retention.id == mock_retention['id']
    assert retention.type == mock_retention['type']


def test_get_pending_collaborations(mock_client, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    expected_url = '{0}/collaborations'.format(API.BASE_API_URL)
    mock_collaboration = {
        'type': 'collaboration',
        'id': '12345',
        'created_by': {
            'type': 'user',
            'id': '33333',
        },
    }
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 1,
        'limit': 2,
        'offset': 0,
        'entries': [mock_collaboration],
    }
    pending_collaborations = mock_client.get_pending_collaborations(limit=2)
    pending_collaboration = pending_collaborations.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'limit': 2, 'status': 'pending', 'offset': None})
    assert isinstance(pending_collaboration, Collaboration)
    assert pending_collaboration.id == mock_collaboration['id']
    assert pending_collaboration.type == mock_collaboration['type']
    assert pending_collaboration['created_by']['type'] == 'user'
    assert pending_collaboration['created_by']['id'] == '33333'


@pytest.fixture
def check_downscope_token_request(
        mock_client,
        mock_box_session,
        mock_object_id,
        make_mock_box_request,
):
    def do_check(item_class, scopes, additional_data, expected_data):
        dummy_downscoped_token = 'dummy_downscoped_token'
        dummy_expires_in = 1234
        mock_box_response, _ = make_mock_box_request(
            response={'access_token': dummy_downscoped_token, 'expires_in': dummy_expires_in},
        )
        mock_box_session.post.return_value = mock_box_response

        item = item_class(mock_box_session, mock_object_id) if item_class else None

        if additional_data:
            downscoped_token_response = mock_client.downscope_token(scopes, item, additional_data)
        else:
            downscoped_token_response = mock_client.downscope_token(scopes, item)

        assert downscoped_token_response.access_token == dummy_downscoped_token
        assert downscoped_token_response.expires_in == dummy_expires_in

        if item:
            expected_data['resource'] = item.get_url()
        mock_box_session.post.assert_called_once_with(
            '{0}/token'.format(API.OAUTH2_API_URL),
            data=expected_data,
        )

    return do_check


@pytest.mark.parametrize(
    'item_class,scopes,expected_scopes',
    [
        (File, [TokenScope.ITEM_READWRITE], 'item_readwrite'),
        (Folder, [TokenScope.ITEM_PREVIEW, TokenScope.ITEM_SHARE], 'item_preview item_share'),
        (File, [TokenScope.ITEM_READ, TokenScope.ITEM_SHARE, TokenScope.ITEM_DELETE], 'item_read item_share item_delete'),
        (None, [TokenScope.ITEM_DOWNLOAD], 'item_download'),
    ],
)
def test_downscope_token_sends_downscope_request(
        mock_client,
        check_downscope_token_request,
        item_class,
        scopes,
        expected_scopes,
):
    expected_data = {
        'subject_token': mock_client.auth.access_token,
        'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
        'scope': expected_scopes,
        'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
    }
    check_downscope_token_request(item_class, scopes, {}, expected_data)


def test_downscope_token_sends_downscope_request_with_additional_data(
        mock_client,
        check_downscope_token_request,
):
    additional_data = {'grant_type': 'new_grant_type', 'extra_data_key': 'extra_data_value'}
    expected_data = {
        'subject_token': mock_client.auth.access_token,
        'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
        'scope': 'item_readwrite',
        'grant_type': 'new_grant_type',
        'extra_data_key': 'extra_data_value',
    }
    check_downscope_token_request(File, [TokenScope.ITEM_READWRITE], additional_data, expected_data)


def test_device_pins_for_enterprise(mock_client, mock_box_session, device_pins_response, device_pin_id_1, device_pin_id_2):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = device_pins_response
    pins = mock_client.device_pinners('1234')
    for pin, expected_id in zip(pins, [device_pin_id_1, device_pin_id_2]):
        assert pin.object_id == expected_id
        # pylint:disable=protected-access
        assert pin._session == mock_box_session
