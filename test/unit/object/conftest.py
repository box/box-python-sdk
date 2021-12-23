# coding: utf-8

import os
from mock import Mock
import pytest
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.collection import Collection
from boxsdk.object.comment import Comment
from boxsdk.object.device_pinner import DevicePinner
from boxsdk.object.file import File
from boxsdk.object.file_version import FileVersion
from boxsdk.object.file_version_retention import FileVersionRetention
from boxsdk.object.legal_hold import LegalHold
from boxsdk.object.folder import Folder
from boxsdk.object.folder_lock import FolderLock
from boxsdk.object.group import Group
from boxsdk.object.group_membership import GroupMembership
from boxsdk.object.legal_hold_policy import LegalHoldPolicy
from boxsdk.object.legal_hold_policy_assignment import LegalHoldPolicyAssignment
from boxsdk.object.metadata_template import MetadataTemplate
from boxsdk.object.user import User
from boxsdk.object.retention_policy import RetentionPolicy
from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment
from boxsdk.object.search import Search
from boxsdk.object.sign_request import SignRequest
from boxsdk.object.storage_policy import StoragePolicy
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment
from boxsdk.object.terms_of_service import TermsOfService
from boxsdk.object.terms_of_service_user_status import TermsOfServiceUserStatus
from boxsdk.object.collaboration_allowlist import CollaborationAllowlist
from boxsdk.object.collaboration_allowlist_entry import CollaborationAllowlistEntry
from boxsdk.object.collaboration_allowlist_exempt_target import CollaborationAllowlistExemptTarget
from boxsdk.object.webhook import Webhook
from boxsdk.object.task import Task
from boxsdk.object.task_assignment import TaskAssignment
from boxsdk.object.web_link import WebLink
from boxsdk.util.default_arg_value import SDK_VALUE_NOT_SET

# pylint:disable=redefined-outer-name


@pytest.fixture(scope='module')
def mock_group_membership_id():
    return 'fake-group-membership-5'


@pytest.fixture(scope='module')
def mock_collaboration_id():
    return 'collab_id1'


@pytest.fixture(scope='module')
def mock_collection_id():
    return 'collection_id1'


@pytest.fixture(scope='module')
def mock_file_path():
    return os.path.join('path', 'to', 'file')


@pytest.fixture(scope='function')
def mock_content_response(make_mock_box_request):
    mock_box_response, mock_network_response = make_mock_box_request(content=b'Contents of a text file.')
    mock_network_response.response_as_stream = raw = Mock()
    raw.stream.return_value = (bytes((b,)) for b in mock_box_response.content)
    return mock_box_response


@pytest.fixture(scope='function', params=[False, True])
def mock_upload_response_contains_entries(request):
    """Is the upload response formatted as {"type": "file", "id": "123", ...}, or as {"entries": [{...}]}.

    The v2.0 API does the latter, but future versions might do the former. So
    we'll test both.
    """
    return request.param


@pytest.fixture(scope='function')
def mock_upload_response(mock_object_id, make_mock_box_request, mock_upload_response_contains_entries):
    response = {'type': 'file', 'id': mock_object_id, 'description': 'Test File Description', }
    if mock_upload_response_contains_entries:
        response = {'entries': [response]}
    mock_box_response, _ = make_mock_box_request(response=response)
    return mock_box_response


@pytest.fixture()
def test_collaboration(mock_box_session, mock_collaboration_id):
    return Collaboration(mock_box_session, mock_collaboration_id)


@pytest.fixture()
def test_file(mock_box_session, mock_object_id):
    return File(mock_box_session, mock_object_id)


@pytest.fixture()
def test_file_version(mock_box_session):
    return FileVersion(mock_box_session, 'file_version_id')


@pytest.fixture()
def test_comment(mock_box_session, mock_object_id):
    return Comment(mock_box_session, mock_object_id)


@pytest.fixture()
def test_collaboration_allowlist(mock_box_session):
    return CollaborationAllowlist(mock_box_session)


@pytest.fixture()
def test_collaboration_allowlist_entry(mock_box_session, mock_object_id):
    return CollaborationAllowlistEntry(mock_box_session, mock_object_id)


@pytest.fixture()
def test_collaboration_allowlist_exemption(mock_box_session, mock_object_id):
    return CollaborationAllowlistExemptTarget(mock_box_session, mock_object_id)


@pytest.fixture()
def test_folder(mock_box_session, mock_object_id):
    return Folder(mock_box_session, mock_object_id)


@pytest.fixture()
def test_group(mock_box_session, mock_group_id):
    return Group(mock_box_session, mock_group_id)


@pytest.fixture()
def test_retention_policy(mock_box_session, mock_object_id):
    return RetentionPolicy(mock_box_session, mock_object_id)


@pytest.fixture()
def test_file_version_retention(mock_box_session, mock_object_id):
    return FileVersionRetention(mock_box_session, mock_object_id)


@pytest.fixture()
def test_retention_policy_assignment(mock_box_session, mock_object_id):
    return RetentionPolicyAssignment(mock_box_session, mock_object_id)


@pytest.fixture()
def test_group_membership(mock_box_session, mock_object_id):
    return GroupMembership(mock_box_session, mock_object_id)


@pytest.fixture()
def test_legal_hold_policy(mock_box_session, mock_object_id):
    return LegalHoldPolicy(mock_box_session, mock_object_id)


@pytest.fixture()
def test_legal_hold_policy_assignment(mock_box_session, mock_object_id):
    return LegalHoldPolicyAssignment(mock_box_session, mock_object_id)


@pytest.fixture()
def test_legal_hold(mock_box_session, mock_object_id):
    return LegalHold(mock_box_session, mock_object_id)


@pytest.fixture()
def test_search(mock_box_session):
    return Search(mock_box_session)


@pytest.fixture()
def test_storage_policy(mock_box_session, mock_object_id):
    return StoragePolicy(mock_box_session, mock_object_id)


@pytest.fixture()
def test_storage_policy_assignment(mock_box_session, mock_object_id):
    return StoragePolicyAssignment(mock_box_session, mock_object_id)


@pytest.fixture()
def test_terms_of_service(mock_box_session, mock_object_id):
    return TermsOfService(mock_box_session, mock_object_id)


@pytest.fixture()
def test_terms_of_service_user_status(mock_box_session, mock_object_id):
    return TermsOfServiceUserStatus(mock_box_session, mock_object_id)


@pytest.fixture()
def test_webhook(mock_box_session, mock_object_id):
    return Webhook(mock_box_session, mock_object_id)


@pytest.fixture()
def test_task(mock_box_session, mock_object_id):
    return Task(mock_box_session, mock_object_id)


@pytest.fixture()
def test_task_assignment(mock_box_session, mock_object_id):
    return TaskAssignment(mock_box_session, mock_object_id)


@pytest.fixture()
def test_web_link(mock_box_session, mock_object_id):
    return WebLink(mock_box_session, mock_object_id)


@pytest.fixture()
def test_device_pin(mock_box_session, mock_object_id):
    return DevicePinner(mock_box_session, mock_object_id)


@pytest.fixture(scope='function')
def mock_collab_response(make_mock_box_request, mock_collaboration_id):
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'collaboration', 'id': mock_collaboration_id},
    )
    return mock_box_response


@pytest.fixture()
def mock_user(mock_box_session, mock_user_id):
    user = User(mock_box_session, mock_user_id)
    return user


@pytest.fixture()
def mock_collection(mock_box_session, mock_collection_id):
    return Collection(mock_box_session, mock_collection_id)


@pytest.fixture(scope='function')
def mock_precondition_failed_response(mock_object_id, make_mock_box_request):
    mock_box_response, _ = make_mock_box_request(
        status_code=412,
        response_ok=False,
        response={'type': 'folder', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture()
def mock_group_membership_dict(mock_group_membership_id, mock_user_id, mock_group_id):
    data = {
        'type': 'group_membership',
        'id': mock_group_membership_id,
        'role': 'member',
        'user': {'type': 'user', 'id': mock_user_id},
        'group': {'type': 'group', 'id': mock_group_id},
    }
    return data


@pytest.fixture()
def mock_add_member_response(mock_group_membership_dict, make_mock_box_request):
    mock_box_response, _ = make_mock_box_request(
        status_code=200,
        response_ok=True,
        response=mock_group_membership_dict,
    )
    return mock_box_response


@pytest.fixture()
def if_match_header(etag):
    return {'If-Match': etag} if etag is not None else None


@pytest.fixture()
def if_none_match_header(etag):
    return {'If-None-Match': etag} if etag is not None else None


@pytest.fixture()
def if_match_sha1_header(etag, sha1):
    headers = {}
    if etag is not None:
        headers['If-Match'] = etag
    if sha1 is not None:
        headers['Content-MD5'] = sha1
    if not headers:
        headers = None
    return headers


@pytest.fixture(params=[None, 'etag'])
def etag(request):
    return request.param


@pytest.fixture(params=[None, 'cf23df2207d99a74fbe169e3eba035e633b65d94'])
def sha1(request):
    return request.param


@pytest.fixture(params=[True, False])
def preflight_check(request):
    return request.param


@pytest.fixture(params=[True, False])
def upload_using_accelerator(request):
    return request.param


@pytest.fixture(params=[True, False])
def preflight_fails(preflight_check, request):
    return preflight_check and request.param


@pytest.fixture(params=[True, False])
def upload_using_accelerator_fails(upload_using_accelerator, request):
    return upload_using_accelerator and request.param


@pytest.fixture(params=[0, 100])
def file_size(request):
    return request.param


@pytest.fixture()
def mock_group(mock_box_session, mock_group_id):
    group = Group(mock_box_session, mock_group_id)
    return group


@pytest.fixture(params=(True, False, None))
def shared_link_can_download(request):
    return request.param


@pytest.fixture(params=(True, False, None))
def shared_link_can_preview(request):
    return request.param


@pytest.fixture(params=('open', None))
def shared_link_access(request):
    return request.param


@pytest.fixture(params=('hunter2', None))
def shared_link_password(request):
    return request.param


@pytest.fixture(params=('2018-10-31', '2018-10-31T23:59:59-07:00', None, SDK_VALUE_NOT_SET))
def shared_link_unshared_at(request):
    return request.param


@pytest.fixture(params=('my-custom-vanity-name', None))
def shared_link_vanity_name(request):
    return request.param


@pytest.fixture(params=[
    # Test case for plain message
    (
        'message',
        'Hello there!'
    ),

    # Test case for tagged message
    (
        'tagged_message',
        '@[22222:Test User] Hi!'
    )
])
def comment_params(request):
    return request.param


@pytest.fixture()
def test_metadata_template(mock_box_session):
    fake_response = {
        'type': 'metadata_template',
        'scope': 'enterprise',
        'templateKey': 'vContract',
    }
    return MetadataTemplate(mock_box_session, None, fake_response)


@pytest.fixture()
def test_folder_lock(mock_box_session, mock_object_id):
    return FolderLock(mock_box_session, mock_object_id)


@pytest.fixture()
def test_sign_request(mock_box_session, mock_object_id):
    return SignRequest(mock_box_session, mock_object_id)
