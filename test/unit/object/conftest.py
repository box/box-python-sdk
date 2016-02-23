# coding: utf-8

from __future__ import unicode_literals
from datetime import date
import os
from mock import Mock
import pytest
from six import int2byte, PY2
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.group import Group
from boxsdk.object.user import User
from boxsdk.object.search import Search


# pylint:disable=redefined-outer-name


@pytest.fixture(scope='module')
def mock_group_membership_id():
    return 'fake-group-membership-5'


@pytest.fixture(scope='module')
def mock_collaboration_id():
    return 'collab_id1'


@pytest.fixture(scope='module')
def mock_file_path():
    return os.path.join('path', 'to', 'file')


@pytest.fixture(scope='function')
def mock_content_response(make_mock_box_request):
    mock_box_response, mock_network_response = make_mock_box_request(content=b'Contents of a text file.')
    mock_network_response.response_as_stream = raw = Mock()
    raw.stream.return_value = (b if PY2 else int2byte(b) for b in mock_box_response.content)
    return mock_box_response


@pytest.fixture(scope='function')
def mock_upload_response(mock_object_id, make_mock_box_request):
    mock_box_response, _ = make_mock_box_request(
        response={'entries': [{'type': 'file', 'id': mock_object_id}]},
    )
    return mock_box_response


@pytest.fixture()
def test_collaboration(mock_box_session, mock_collaboration_id):
    return Collaboration(mock_box_session, mock_collaboration_id)


@pytest.fixture()
def test_file(mock_box_session, mock_object_id):
    return File(mock_box_session, mock_object_id)


@pytest.fixture()
def test_folder(mock_box_session, mock_object_id):
    return Folder(mock_box_session, mock_object_id)


@pytest.fixture()
def test_group(mock_box_session, mock_group_id):
    return Group(mock_box_session, mock_group_id)


@pytest.fixture()
def test_search(mock_box_session):
    return Search(mock_box_session)


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


@pytest.fixture(params=[None, 'etag'])
def etag(request):
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


@pytest.fixture(params=(date(2015, 5, 5), None))
def shared_link_unshared_at(request):
    return request.param
