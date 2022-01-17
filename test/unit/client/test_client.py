# coding: utf-8
# pylint: disable=too-many-lines

import json
from io import BytesIO

from mock import Mock, ANY
import pytest


from boxsdk.auth.oauth2 import OAuth2, TokenScope
from boxsdk.client import Client, DeveloperTokenClient, DevelopmentClient, LoggingClient
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.collaboration_allowlist import CollaborationAllowlist
from boxsdk.object.email_alias import EmailAlias
from boxsdk.object.collection import Collection
from boxsdk.object.comment import Comment
from boxsdk.object.device_pinner import DevicePinner
from boxsdk.object.enterprise import Enterprise
from boxsdk.object.events import Events
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.object.file_version import FileVersion
from boxsdk.object.group import Group
from boxsdk.object.invite import Invite
from boxsdk.object.storage_policy import StoragePolicy
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment
from boxsdk.object.terms_of_service import TermsOfService
from boxsdk.object.user import User
from boxsdk.object.upload_session import UploadSession
from boxsdk.object.trash import Trash
from boxsdk.object.group_membership import GroupMembership
from boxsdk.object.metadata_template import MetadataTemplate, MetadataField, MetadataFieldType
from boxsdk.object.retention_policy import RetentionPolicy
from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment
from boxsdk.object.file_version_retention import FileVersionRetention
from boxsdk.object.legal_hold import LegalHold
from boxsdk.object.legal_hold_policy import LegalHoldPolicy
from boxsdk.object.legal_hold_policy_assignment import LegalHoldPolicyAssignment
from boxsdk.object.metadata_cascade_policy import MetadataCascadePolicy
from boxsdk.object.sign_request import SignRequest
from boxsdk.object.task import Task
from boxsdk.object.task_assignment import TaskAssignment
from boxsdk.object.webhook import Webhook
from boxsdk.object.web_link import WebLink
from boxsdk.pagination.marker_based_object_collection import MarkerBasedObjectCollection


@pytest.fixture
def developer_token_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda prompt: 'developer_token')


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


@pytest.fixture(scope='function')
def mock_content_response(make_mock_box_request):
    mock_box_response, mock_network_response = make_mock_box_request(content=b'Contents of a text file.')
    mock_network_response.response_as_stream = raw = Mock()
    raw.stream.return_value = (bytes((b,)) for b in mock_box_response.content)
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
            {'type': 'group', 'id': group_id_1, 'name': str(group_id_1)},
            {'type': 'group', 'id': group_id_2, 'name': str(group_id_2)},
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
def tos_id_1():
    return 101


@pytest.fixture(scope='module')
def tos_id_2():
    return 202


@pytest.fixture(scope='module')
def terms_of_services_response(tos_id_1, tos_id_2):
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'terms_of_service', 'id': tos_id_1},
            {'type': 'terms_of_service', 'id': tos_id_2},
        ],
        'total_count': 2,
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


@pytest.fixture(scope='module')
def create_invite_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'type': 'invite',
        'id': 1234,
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
    (EmailAlias, 'email_alias'),
    (Enterprise, 'enterprise'),
    (Folder, 'folder'),
    (File, 'file'),
    (FileVersion, 'file_version'),
    (Invite, 'invite'),
    (User, 'user'),
    (Group, 'group'),
    (GroupMembership, 'group_membership'),
    (Enterprise, 'enterprise'),
    (Webhook, 'webhook'),
    (MetadataCascadePolicy, 'metadata_cascade_policy'),
    (UploadSession, 'upload_session'),
    (StoragePolicy, 'storage_policy'),
    (StoragePolicyAssignment, 'storage_policy_assignment'),
])
def test_factory_returns_the_correct_object(mock_client, test_class, factory_method_name):
    """ Tests the various id-only factory methods in the Client class """
    # pylint:disable=redefined-outer-name
    fake_id = 'fake_id'

    factory_method = getattr(mock_client, factory_method_name)

    obj = factory_method(fake_id)

    assert isinstance(obj, test_class)
    assert obj.object_id == fake_id


def test_root_folder(mock_client):
    folder = mock_client.root_folder()
    assert isinstance(folder, Folder)
    assert folder.object_id == '0'


@pytest.fixture(scope='module', params=(None, 'user1'))
def users_filter_term(request):
    return request.param


@pytest.fixture(scope='module', params=(0, 10))
def users_offset(request):
    return request.param


@pytest.fixture(scope='module', params=(0, 10))
def users_limit(request):
    return request.param


@pytest.fixture(scope='module', params=(None, 'all', 'external', 'managed'))
def users_type(request):
    return request.param


def test_users_return_the_correct_user_objects(
        mock_client,
        mock_box_session,
        users_response,
        user_id_1,
        user_id_2,
        users_filter_term,
        users_type,
        users_offset,
        users_limit,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = users_response
    users = mock_client.users(limit=users_limit, offset=users_offset, filter_term=users_filter_term, user_type=users_type)
    expected_params = {'offset': users_offset}
    if users_limit is not None:
        expected_params['limit'] = users_limit
    if users_filter_term is not None:
        expected_params['filter_term'] = users_filter_term
    if users_type is not None:
        expected_params['user_type'] = users_type
    assert users.next().object_id == user_id_1
    assert users.next().object_id == user_id_2
    mock_box_session.get.assert_called_once_with(f'{API.BASE_API_URL}/users', params=expected_params)


def test_users_return_the_correct_user_objects_marker(
        mock_client,
        mock_box_session,
        user_id_1,
        user_id_2,
        users_filter_term,
        users_type,
        marker_id,
        users_limit,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value.json.return_value = {
        'entries': [
            {'type': 'user', 'id': user_id_1},
            {'type': 'user', 'id': user_id_2}
        ],
        'next_marker': 'JGWUGKNJFSAH123NDSA',
        'total_count': 2
    }
    users = mock_client.users(limit=users_limit, marker=marker_id, use_marker=True, filter_term=users_filter_term, user_type=users_type)
    expected_params = {'marker': marker_id, 'usemarker': True}
    if users_limit is not None:
        expected_params['limit'] = users_limit
    if users_filter_term is not None:
        expected_params['filter_term'] = users_filter_term
    if users_type is not None:
        expected_params['user_type'] = users_type
    assert users.next().object_id == user_id_1
    assert users.next().object_id == user_id_2
    mock_box_session.get.assert_called_once_with(f'{API.BASE_API_URL}/users', params=expected_params)


def test_users_returns_correct_with_default_values(
        mock_client,
        mock_box_session,
):
    expected_url = f'{API.BASE_API_URL}/users'
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'offset': 0,
        'total_count': 1,
        'entries': [
            {
                'type': 'user',
                'id': '12345',
            }
        ]
    }
    users = mock_client.users()
    user = users.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': 0})
    assert isinstance(user, User)
    assert user.type == 'user'
    assert user.id == '12345'


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
    search_result = mock_client.search().query(
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


def test_collaboration_allowlist_initializer(mock_client):
    collaboration_allowlist = mock_client.collaboration_allowlist()
    assert isinstance(collaboration_allowlist, CollaborationAllowlist)


def test_get_groups_return_the_correct_group_objects(
        mock_client,
        mock_box_session,
        groups_response,
        group_id_1,
        group_id_2,
):
    # pylint:disable=redefined-outer-name
    group_name = 'Employees'
    expected_url = f'{API.BASE_API_URL}/groups'
    mock_box_session.get.return_value = groups_response
    groups = mock_client.get_groups(group_name)
    for group, expected_id in zip(groups, [group_id_1, group_id_2]):
        assert group.object_id == expected_id
        assert group.name == str(expected_id)
        # pylint:disable=protected-access
        assert group._session == mock_box_session
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': None, 'filter_term': group_name})


def test_create_group_returns_the_correct_group_object(mock_client, mock_box_session, create_group_response):
    # pylint:disable=redefined-outer-name
    expected_url = f'{API.BASE_API_URL}/groups'
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
        fields=['name,description'],
    )

    mock_box_session.post.assert_called_once_with(expected_url, data=value, params={'fields': 'name,description'})
    assert isinstance(new_group, Group)
    assert new_group.object_id == 1234
    assert new_group.name == test_group_name


@pytest.mark.parametrize('params', [
    {
        'description': 'My test policy',
    },
    {
        'filter_starting_at': '2016-01-01T00:00:00Z',
        'filter_ending_at': '2020-01-01T00:00:00Z',
    },
    {
        'is_ongoing': True,
    }
])
def test_create_legal_hold_policy_returns_the_correct_policy_object(mock_client, mock_box_session, create_policy_response, params):
    # pylint:disable=redefined-outer-name
    test_policy_name = 'Test Policy'
    expected_url = f'{API.BASE_API_URL}/legal_hold_policies'
    expected_body = {
        'policy_name': test_policy_name
    }
    expected_body.update(params)
    value = json.dumps(expected_body)
    create_policy_response.json.return_value.update(params)
    mock_box_session.post.return_value = create_policy_response
    new_policy = mock_client.create_legal_hold_policy(test_policy_name, **params)
    mock_box_session.post.assert_called_once_with(expected_url, data=ANY)
    assert dict(json.loads(mock_box_session.post.call_args[1]['data'])) == dict(json.loads(value))
    assert isinstance(new_policy, LegalHoldPolicy)
    assert new_policy.policy_name == test_policy_name
    for param in params:
        assert new_policy[param] == params[param]


def test_get_legal_hold_policies_return_the_correct_policy_objects(
        mock_client,
        mock_box_session,
        legal_hold_policies_response,
        legal_hold_policy_id_1,
        legal_hold_policy_id_2,
):
    # pylint:disable=redefined-outer-name
    policy_name = 'Arbitration'
    expected_url = f'{API.BASE_API_URL}/legal_hold_policies'
    mock_box_session.get.return_value = legal_hold_policies_response
    policies = mock_client.get_legal_hold_policies(policy_name)
    for policy, expected_id in zip(policies, [legal_hold_policy_id_1, legal_hold_policy_id_2]):
        assert policy.object_id == expected_id
        # pylint:disable=protected-access
        assert policy._session == mock_box_session
    mock_box_session.get.assert_called_once_with(expected_url, params={'policy_name': policy_name})


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
    mock_box_session.get.assert_called_once_with(f'{API.BASE_API_URL}/recent_items', params=expected_params)


@pytest.mark.parametrize('password', (None, 'p4ssw0rd'))
def test_get_shared_item_returns_the_correct_item(mock_client, mock_box_session, shared_item_response, password):
    # pylint:disable=redefined-outer-name
    shared_link = 'https://cloud.box.com/s/661wcw2iz6q5r7v5xxkm'
    mock_box_session.request.return_value = shared_item_response
    item = mock_client.get_shared_item(shared_link, password)
    assert item.type == shared_item_response.json()['type']
    mock_box_session.request.assert_called_once_with(
        'GET',
        f'{API.BASE_API_URL}/shared_items',
        headers={
            'BoxApi': f'shared_link={shared_link}{f"&shared_link_password={password}" if password is not None else ""}'
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

    assert mock_box_session.post.call_args[0] == (f'{API.BASE_API_URL}/users',)
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

    assert mock_box_session.post.call_args[0] == (f"{API.BASE_API_URL}/users",)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_user, User)
    assert new_user.object_id == 1234
    assert new_user.name == test_user_name


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
    policies = mock_client.get_storage_policies()
    policy = policies.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(policy, StoragePolicy)
    assert policy.type == 'storage_policy'
    assert policy.id == '12345'
    assert policy.name == 'Test Storage Policy'


def test_create_terms_of_service(mock_client, mock_box_session):
    # pylint:disable=redefined-outer-name
    expected_url = f'{API.BASE_API_URL}/terms_of_services'
    test_text = 'This is a test text'
    test_tos_type = 'external'
    test_status = 'enabled'
    value = json.dumps({
        'status': 'enabled',
        'tos_type': 'external',
        'text': 'This is a test text',
    })
    mock_box_session.post.return_value.json.return_value = {
        'type': 'terms_of_service',
        'id': '12345',
        'status': test_status,
        'tos_type': test_tos_type,
        'text': test_text,
    }
    new_terms_of_service = mock_client.create_terms_of_service('enabled', 'external', 'This is a test text')
    mock_box_session.post.assert_called_once_with(expected_url, data=value)
    assert isinstance(new_terms_of_service, TermsOfService)
    assert new_terms_of_service.type == 'terms_of_service'
    assert new_terms_of_service.id == '12345'
    assert new_terms_of_service.status == test_status
    assert new_terms_of_service.tos_type == test_tos_type
    assert new_terms_of_service.text == test_text


def test_get_all_terms_of_services(mock_client, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/terms_of_services'
    tos_body = {
        'type': 'terms_of_service',
        'id': '12345',
        'status': 'enabled',
        'tos_type': 'external',
    }
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 1,
        'entries': [tos_body],
    }
    services = mock_client.get_terms_of_services(tos_type='external')
    service = services.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'tos_type': 'external'})
    assert isinstance(service, TermsOfService)
    assert service.type == 'terms_of_service'
    assert service.id == '12345'
    assert service.status == 'enabled'
    assert service.tos_type == 'external'


def test_create_webhook_returns_the_correct_policy_object(
        test_item_and_response,
        test_webhook,
        mock_client,
        mock_box_session,
        create_webhook_response,
):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = f'{API.BASE_API_URL}/webhooks'
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
    expected_url = f'{API.BASE_API_URL}/webhooks'
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
    expected_url = f'{API.BASE_API_URL}/retention_policies'
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
    expected_url = f'{API.BASE_API_URL}/retention_policies'.format()
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
    expected_url = f'{API.BASE_API_URL}/retention_policies'
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
    expected_url = f'{API.BASE_API_URL}/file_version_retentions'
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
    expected_url = f'{API.BASE_API_URL}/collaborations'
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
    def do_check(scopes, item_class, additional_data, shared_link, expected_data):
        temp_downscoped_token = 'temp_downscoped_token'
        temp_expires_in = 1234
        mock_box_response, _ = make_mock_box_request(
            response={'access_token': temp_downscoped_token, 'expires_in': temp_expires_in},
        )
        mock_box_session.post.return_value = mock_box_response

        item = item_class(mock_box_session, mock_object_id) if item_class else None

        downscoped_token_response = mock_client.downscope_token(scopes, item, additional_data, shared_link)

        assert downscoped_token_response.access_token == temp_downscoped_token
        assert downscoped_token_response.expires_in == temp_expires_in

        if item:
            expected_data['resource'] = item.get_url()
        mock_box_session.post.assert_called_once_with(f'{API.OAUTH2_API_URL}/token', data=expected_data)

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
    mock_client.auth.access_token = 'existing_access_token'
    expected_data = {
        'subject_token': 'existing_access_token',
        'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
        'scope': expected_scopes,
        'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
    }
    check_downscope_token_request(scopes, item_class, None, None, expected_data)


def test_downscope_token_sends_downscope_request_with_shared_link(
        mock_client,
        check_downscope_token_request,
):
    shared_link = 'https://cloud.box.com/s/foo'
    expected_data = {
        'subject_token': mock_client.auth.access_token,
        'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
        'scope': 'item_readwrite',
        'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
        'box_shared_link': shared_link
    }
    check_downscope_token_request([TokenScope.ITEM_READWRITE], None, None, shared_link, expected_data)


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
    check_downscope_token_request([TokenScope.ITEM_READWRITE], File, additional_data, None, expected_data)


def test_downscope_token_sends_downscope_request_when_no_initial_token(
        mock_client,
        check_downscope_token_request,
):
    mock_client.auth.access_token = None
    mock_client.auth.refresh.return_value = 'new_access_token'

    expected_data = {
        'subject_token': 'new_access_token',
        'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
        'scope': 'item_readwrite',
        'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
    }
    check_downscope_token_request([TokenScope.ITEM_READWRITE], File, None, None, expected_data)
    mock_client.auth.refresh.assert_called_once_with(None)


def test_device_pins_for_enterprise(mock_client, mock_box_session, device_pins_response, device_pin_id_1, device_pin_id_2):
    # pylint:disable=redefined-outer-name
    enterprise_id = '11111'
    expected_url = f'{API.BASE_API_URL}/enterprises/{enterprise_id}/device_pinners'
    mock_box_session.get.return_value = device_pins_response
    enterprise = mock_client.enterprise(enterprise_id)
    pins = mock_client.device_pinners(enterprise, direction='ASC')
    for pin, expected_id in zip(pins, [device_pin_id_1, device_pin_id_2]):
        assert pin.object_id == expected_id
        # pylint:disable=protected-access
        assert pin._session == mock_box_session
    mock_box_session.get.assert_called_once_with(expected_url, params={'direction': 'ASC'})


def test_metadata_template_initializer(mock_client, mock_box_session):
    template = mock_client.metadata_template('enterprise', 'VendorContract')
    assert isinstance(template, MetadataTemplate)
    # pylint:disable=protected-access
    assert template._session == mock_box_session
    assert template.object_id is None
    assert template.scope == 'enterprise'
    assert template.template_key == 'VendorContract'


def test_metadata_template_by_id(mock_client, mock_box_session):
    template_id = 'sdkjfhgsdg-nb34745bndfg-qw4hbsajdg'

    template = mock_client.metadata_template_by_id(template_id)

    assert isinstance(template, MetadataTemplate)
    # pylint:disable=protected-access
    assert template._session == mock_box_session
    assert template.object_id == template_id
    assert template.scope is None
    assert template.template_key is None


def test_get_metadata_templates(mock_client, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_templates/enterprise'
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 1,
        'entries': [
            {
                'type': 'metadata_template',
                'scope': 'enterprise_33333',
                'displayName': 'Vendor Contract',
                'templateKey': 'vendorContract',
                'fields': [
                    {
                        'type': 'string',
                        'displayName': 'Name',
                        'key': 'name',
                    },
                ],
            },
        ],
        'next_marker': None,
        'previous_marker': None,
    }

    templates = mock_client.get_metadata_templates()
    template = templates.next()

    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(template, MetadataTemplate)
    assert template.object_id is None
    assert template.displayName == 'Vendor Contract'
    fields = template.fields
    assert len(fields) == 1
    field = fields[0]
    assert isinstance(field, dict)
    assert field['type'] == 'string'
    assert field['key'] == 'name'


def test_create_metadata_template(mock_client, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_templates/schema'
    name = 'Vendor Contract'
    key = 'vContract'
    field1 = MetadataField(MetadataFieldType.DATE, 'Birthday', 'bday')
    field2 = MetadataField(MetadataFieldType.ENUM, 'State', options=['CA', 'TX', 'NY'])
    expected_body = {
        'scope': 'enterprise',
        'displayName': 'Vendor Contract',
        'hidden': True,
        'fields': [
            {
                'type': 'date',
                'displayName': 'Birthday',
                'key': 'bday',
            },
            {
                'type': 'enum',
                'displayName': 'State',
                'options': [
                    {'key': 'CA'},
                    {'key': 'TX'},
                    {'key': 'NY'},
                ],
            },
        ],
        'copyInstanceOnItemCopy': False,
        'templateKey': 'vContract',
    }

    response = {
        'type': 'metadata_template',
    }
    response.update(expected_body)
    mock_box_session.post.return_value.json.return_value = response

    template = mock_client.create_metadata_template(name, [field1, field2], key, hidden=True)

    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(template, MetadataTemplate)
    assert template.object_id is None
    assert template.displayName == 'Vendor Contract'
    fields = template.fields
    assert len(fields) == 2
    field = fields[0]
    assert isinstance(field, dict)
    assert field['type'] == 'date'
    assert field['key'] == 'bday'


def test_get_current_enterprise(mock_client, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/users/me'
    expected_params = {
        'fields': 'enterprise'
    }
    enterprise_id = '44444'
    enterprise_name = 'Acme, Inc.'
    user_json = {
        'type': 'user',
        'id': '33333',
        'enterprise': {
            'type': 'enterprise',
            'id': enterprise_id,
            'name': enterprise_name,
        },
    }
    mock_box_session.get.return_value.json.return_value = user_json

    enterprise = mock_client.get_current_enterprise()

    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params, headers=None)
    assert isinstance(enterprise, Enterprise)
    assert enterprise.object_id == enterprise_id
    assert enterprise._session == mock_box_session  # pylint:disable=protected-access
    assert enterprise.name == enterprise_name
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params={'fields': 'enterprise'})


def test_comment(mock_client):
    # pylint:disable=redefined-outer-name
    comment_id = '12345'
    comment = mock_client.comment(comment_id)

    assert isinstance(comment, Comment)
    assert comment.object_id == comment_id


def test_collaboration(mock_client):
    # pylint:disable=redefined-outer-name
    collaboration_id = '12345'
    collaboration = mock_client.collaboration(collaboration_id)

    assert isinstance(collaboration, Collaboration)
    assert collaboration.object_id == collaboration_id


def test_legal_hold_policy(mock_client):
    # pylint:disable=redefined-outer-name
    policy_id = '12345'
    policy = mock_client.legal_hold_policy(policy_id)

    assert isinstance(policy, LegalHoldPolicy)
    assert policy.object_id == policy_id


def test_legal_hold_policy_assignment(mock_client):
    # pylint:disable=redefined-outer-name
    assignment_id = '12345'
    assignment = mock_client.legal_hold_policy_assignment(assignment_id)

    assert isinstance(assignment, LegalHoldPolicyAssignment)
    assert assignment.object_id == assignment_id


def test_legal_hold(mock_client):
    # pylint:disable=redefined-outer-name
    hold_id = '12345'
    legal_hold = mock_client.legal_hold(hold_id)

    assert isinstance(legal_hold, LegalHold)
    assert legal_hold.object_id == hold_id


def test_collection(mock_client):
    # pylint:disable=redefined-outer-name
    collection_id = '12345'
    collection = mock_client.collection(collection_id)

    assert isinstance(collection, Collection)
    assert collection.object_id == collection_id


def test_collections(mock_client, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    expected_url = f'{API.BASE_API_URL}/collections'
    mock_collection = {
        'type': 'collection',
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
        'entries': [mock_collection],
    }
    collections = mock_client.collections(limit=2)
    collection = collections.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'limit': 2, 'offset': 0})
    assert isinstance(collection, Collection)
    assert collection.id == mock_collection['id']
    assert collection.type == mock_collection['type']
    assert collection['created_by']['type'] == 'user'
    assert collection['created_by']['id'] == '33333'


def test_task(mock_client):
    # pylint:disable=redefined-outer-name
    task_id = '12345'
    task = mock_client.task(task_id)

    assert isinstance(task, Task)
    assert task.object_id == task_id


def test_task_assignment(mock_client):
    # pylint:disable=redefined-outer-name
    assignment_id = '12345'
    assignment = mock_client.task_assignment(assignment_id)

    assert isinstance(assignment, TaskAssignment)
    assert assignment.object_id == assignment_id


def test_retention_policy(mock_client):
    # pylint:disable=redefined-outer-name
    policy_id = '12345'
    policy = mock_client.retention_policy(policy_id)

    assert isinstance(policy, RetentionPolicy)
    assert policy.object_id == policy_id


def test_retention_policy_assignment(mock_client):
    # pylint:disable=redefined-outer-name
    assignment_id = '12345'
    assignment = mock_client.retention_policy_assignment(assignment_id)

    assert isinstance(assignment, RetentionPolicyAssignment)
    assert assignment.object_id == assignment_id


def test_file_version_retention(mock_client):
    # pylint:disable=redefined-outer-name
    retention_id = '12345'
    file_version_retention = mock_client.file_version_retention(retention_id)

    assert isinstance(file_version_retention, FileVersionRetention)
    assert file_version_retention.object_id == retention_id


def test_web_link(mock_client):
    # pylint:disable=redefined-outer-name
    web_link_id = '12345'
    web_link = mock_client.web_link(web_link_id)

    assert isinstance(web_link, WebLink)
    assert web_link.object_id == web_link_id


def test_device_pinner(mock_client):
    # pylint:disable=redefined-outer-name
    pin_id = '12345'
    pin = mock_client.device_pinner(pin_id)

    assert isinstance(pin, DevicePinner)
    assert pin.object_id == pin_id


def test_download_zip(mock_client, mock_box_session, mock_content_response):
    expected_create_url = f'{API.BASE_API_URL}/zip_downloads'
    name = 'test'
    file_item = mock_client.file('466239504569')
    folder_item = mock_client.folder('466239504580')
    items = [file_item, folder_item]
    mock_writeable_stream = BytesIO()
    expected_create_body = {
        'download_file_name': name,
        'items': [
            {
                'type': 'file',
                'id': '466239504569'
            },
            {
                'type': 'folder',
                'id': '466239504580'
            }
        ]
    }
    status_response_mock = Mock()
    status_response_mock.json.return_value = {
        'total_file_count': 20,
        'downloaded_file_count': 10,
        'skipped_file_count': 10,
        'skipped_folder_count': 10,
        'state': 'succeeded'
    }
    mock_box_session.post.return_value.json.return_value = {
        'download_url': 'https://dl.boxcloud.com/2.0/zip_downloads/124hfiowk3fa8kmrwh/content',
        'status_url': 'https://api.box.com/2.0/zip_downloads/124hfiowk3fa8kmrwh/status',
        'expires_at': '2018-04-25T11:00:18-07:00',
        'name_conflicts': [
            [
                {
                    'id': '100',
                    'type': 'file',
                    'original_name': 'salary.pdf',
                    'download_name': 'aqc823.pdf'
                },
                {
                    'id': '200',
                    'type': 'file',
                    'original_name': 'salary.pdf',
                    'download_name': 'aci23s.pdf'
                }
            ]
        ]
    }

    mock_box_session.get.side_effect = [mock_content_response, status_response_mock]

    status_returned = mock_client.download_zip(name, items, mock_writeable_stream)
    mock_box_session.post.assert_called_once_with(expected_create_url, data=json.dumps(expected_create_body))
    mock_box_session.get.assert_any_call('https://dl.boxcloud.com/2.0/zip_downloads/124hfiowk3fa8kmrwh/content',
                                         expect_json_response=False, stream=True)
    mock_box_session.get.assert_called_with('https://api.box.com/2.0/zip_downloads/124hfiowk3fa8kmrwh/status')
    mock_writeable_stream.seek(0)
    assert mock_writeable_stream.read() == mock_content_response.content
    assert status_returned['total_file_count'] == 20
    assert status_returned['name_conflicts'][0][0]['id'] == '100'


@pytest.fixture(scope='module')
def mock_sign_request_response():
    # pylint:disable=redefined-outer-name
    mock_sign_request = {
        'id': '42',
        'type': 'sign-request',
        'are_reminders_enabled': 'true',
        'are_text_signatures_enabled': 'true',
        'auto_expire_at': '2021-04-26T08:12:13.982Z',
        'days_valid': '2',
        'email_message': 'Hello! Please sign the document below',
        'email_subject': 'Sign Request from Acme',
        'external_id': '123',
        'is_document_preparation_needed': 'true',
        'parent_folder': {
            'id': '12345',
            'type': 'folder',
            'etag': '1',
            'name': 'Contracts',
            'sequence_id': '3'
        },
        'prefill_tags': [
            {
                'document_tag_id': '1234',
                'text_value': 'text',
                'checkbox_value': 'true',
                'date_value': '2021-04-26T08:12:13.982Z'
            }
        ],
        'prepare_url': 'https://prepareurl.com',
        'sign_files': {
            'files': [
                {
                    'id': '12345',
                    'etag': '1',
                    'type': 'file',
                    'sequence_id': '3',
                    'name': 'Contract.pdf',
                    'sha1': '85136C79CBF9FE36BB9D05D0639C70C265C18D37',
                    'file_version': {
                        'id': '12345',
                        'type': 'file_version',
                        'sha1': '134b65991ed521fcfe4724b7d814ab8ded5185dc'
                    }
                }
            ],
            'is_ready_for_download': 'true'
        },
        'signers': [
            {
                'email': 'example@gmail.com',
                'role': 'signer',
                'is_in_person': 'true',
                'order': '2',
                'embed_url_external_user_id': '1234',
                'has_viewed_document': 'true',
                'signer_decision': {
                    'type': 'signed',
                    'finalized_at': '2021-04-26T08:12:13.982Z'
                },
                'inputs': [
                    {
                        'document_tag_id': '1234',
                        'text_value': 'text',
                        'checkbox_value': 'true',
                        'date_value': '2021-04-26T08:12:13.982Z',
                        'type': 'text',
                        'page_index': '4'
                    }
                ],
                'embed_url': 'https://example.com'
            }
        ],
        'signing_log': {
            'id': '12345',
            'type': 'file',
            'etag': '1',
            'file_version': {
                'id': '12345',
                'type': 'file_version',
                'sha1': '134b65991ed521fcfe4724b7d814ab8ded5185dc'
            },
            'name': 'Contract.pdf',
            'sequence_id': '3',
            'sha1': '85136C79CBF9FE36BB9D05D0639C70C265C18D37'
        },
        'source_files': [
            {
                'id': '12345',
                'etag': '1',
                'type': 'file',
                'sequence_id': '3',
                'name': 'Contract.pdf',
                'sha1': '85136C79CBF9FE36BB9D05D0639C70C265C18D37',
                'file_version': {
                    'id': '12345',
                    'type': 'file_version',
                    'sha1': '134b65991ed521fcfe4724b7d814ab8ded5185dc'
                }
            }
        ],
        'status': 'converting'
    }
    return mock_sign_request


def test_get_sign_requests(mock_client, mock_box_session, mock_sign_request_response):
    expected_url = f'{API.BASE_API_URL}/sign_requests'

    mock_sign_request = mock_sign_request_response
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 1,
        'limit': 100,
        'entries': [mock_sign_request],
        'next_marker': None,
        'previous_marker': None,
    }

    sign_requests = mock_client.get_sign_requests()
    sign_request = sign_requests.next()

    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(sign_request, SignRequest)
    assert sign_request.id == mock_sign_request['id']
    assert sign_request.status == mock_sign_request['status']


def test_create_sign_request(mock_client, mock_box_session, mock_sign_request_response):
    expected_url = f'{API.BASE_API_URL}/sign_requests'

    source_file = {
        'id': '12345',
        'type': 'file'
    }
    files = [source_file]

    signer = {
        'email': 'example@gmail.com'
    }
    signers = [signer]
    parent_folder_id = '12345'

    data = json.dumps({
        'source_files': [
            {
                'id': source_file['id'],
                'type': source_file['type']
            }
        ],
        'signers': [
            {
                'email': signer['email']
            }
        ],
        'parent_folder':
        {
            'id': parent_folder_id,
            'type': 'folder'
        }
    })
    mock_box_session.post.return_value.json.return_value = mock_sign_request_response

    new_sign_request = mock_client.create_sign_request(
        files, signers, parent_folder_id)

    mock_box_session.post.assert_called_once_with(expected_url, data=data)
    assert isinstance(new_sign_request, SignRequest)
    assert new_sign_request['source_files'][0]['id'] == source_file['id']
    assert new_sign_request['signers'][0]['email'] == signer['email']
    assert new_sign_request['parent_folder']['id'] == parent_folder_id
