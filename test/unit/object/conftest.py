# coding: utf-8

from __future__ import unicode_literals
import json
import os
from mock import Mock
import pytest
from six import int2byte, PY2
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.group import Group
from boxsdk.object.user import User
from boxsdk.session.box_session import BoxResponse


@pytest.fixture(scope='module')
def mock_object_id():
    return '42'


@pytest.fixture(scope='module')
def mock_user_id():
    return 'fake-user-100'


@pytest.fixture(scope='module')
def mock_group_id():
    return 'fake-group-99'


@pytest.fixture(scope='module')
def mock_group_membership_id():
    return 'fake-group-membership-5'


@pytest.fixture(scope='module')
def mock_collaboration_id():
    return 'collab_id1'


@pytest.fixture(scope='module')
def mock_file_path():
    return os.path.join('path', 'to', 'file')


@pytest.fixture()
def make_mock_box_request():
    def inner(status_code=200, response_ok=True, response=None, content=None):
        mock_box_response = Mock(BoxResponse)
        mock_network_response = Mock(DefaultNetworkResponse)
        mock_box_response.network_response = mock_network_response
        mock_box_response.status_code = status_code
        mock_box_response.ok = response_ok
        if response is not None:
            mock_box_response.json.return_value = response
            mock_box_response.content = json.dumps(response).encode()
        else:
            mock_box_response.content = content
        return mock_box_response, mock_network_response
    return inner


@pytest.fixture(scope='function')
def mock_content_response(make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, mock_network_response = make_mock_box_request(content=b'Contents of a text file.')
    mock_network_response.response_as_stream = raw = Mock()
    raw.stream.return_value = (b if PY2 else int2byte(b) for b in mock_box_response.content)
    return mock_box_response


@pytest.fixture(scope='function')
def mock_upload_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'entries': [{'type': 'file', 'id': mock_object_id}]},
    )
    return mock_box_response


@pytest.fixture(scope='function')
def mock_file_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'file', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture()
def test_collaboration(mock_box_session, mock_collaboration_id):
    # pylint:disable=redefined-outer-name
    return Collaboration(mock_box_session, mock_collaboration_id)


@pytest.fixture()
def test_file(mock_box_session, mock_object_id):
    # pylint:disable=redefined-outer-name
    return File(mock_box_session, mock_object_id)


@pytest.fixture()
def test_folder(mock_box_session, mock_object_id):
    # pylint:disable=redefined-outer-name
    return Folder(mock_box_session, mock_object_id)


@pytest.fixture()
def test_group(mock_box_session, mock_group_id):
    # pylint:disable=redefined-outer-name
    return Group(mock_box_session, mock_group_id)


@pytest.fixture(scope='function')
def mock_folder_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'folder', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture(scope='function')
def mock_collab_response(make_mock_box_request, mock_collaboration_id):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'collaboration', 'id': mock_collaboration_id},
    )
    return mock_box_response


@pytest.fixture()
def mock_user(mock_box_session, mock_user_id):
    # pylint:disable=redefined-outer-name
    user = User(mock_box_session, mock_user_id)
    return user


@pytest.fixture(scope='function')
def mock_user_response(mock_user_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'user', 'id': mock_user_id},
    )
    return mock_box_response


@pytest.fixture(scope='function')
def mock_precondition_failed_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        status_code=412,
        response_ok=False,
        response={'type': 'folder', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture()
def mock_group_membership_dict(mock_group_membership_id, mock_user_id, mock_group_id):
    # pylint:disable=redefined-outer-name
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
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        status_code=200,
        response_ok=True,
        response=mock_group_membership_dict,
    )
    return mock_box_response


@pytest.fixture()
def if_match_header(etag):
    # pylint:disable=redefined-outer-name
    return {'If-Match': etag} if etag is not None else None


@pytest.fixture()
def if_none_match_header(etag):
    # pylint:disable=redefined-outer-name
    return {'If-None-Match': etag} if etag is not None else None


@pytest.fixture(params=[None, 'etag'])
def etag(request):
    return request.param


@pytest.fixture()
def mock_group(mock_box_session, mock_group_id):
    # pylint:disable=redefined-outer-name
    group = Group(mock_box_session, mock_group_id)
    return group
