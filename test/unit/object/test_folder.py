# coding: utf-8

from __future__ import unicode_literals
import json
from os.path import basename
from mock import mock_open, patch, Mock
import pytest
from six import BytesIO
from six.moves import zip  # pylint:disable=redefined-builtin,import-error
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.file import File
from boxsdk.object.collaboration import Collaboration, CollaborationRole
from boxsdk.object.folder import Folder, FolderSyncState
from boxsdk.session.box_session import BoxResponse


# pylint:disable=protected-access


@pytest.fixture()
def mock_items(mock_box_session, mock_object_id):
    return [
        {'type': 'file', 'id': mock_object_id},
        {'type': 'folder', 'id': mock_object_id},
        {'type': 'file', 'id': mock_object_id},
    ], [
        File(mock_box_session, mock_object_id),
        Folder(mock_box_session, mock_object_id),
        File(mock_box_session, mock_object_id),
    ]


@pytest.fixture()
def mock_items_response(mock_items):
    # pylint:disable=redefined-outer-name
    def get_response(limit, offset):
        items_json, items = mock_items
        mock_box_response = Mock(BoxResponse)
        mock_network_response = Mock(DefaultNetworkResponse)
        mock_box_response.network_response = mock_network_response
        mock_box_response.json.return_value = mock_json = {'entries': items_json[offset:limit + offset]}
        mock_box_response.content = json.dumps(mock_json).encode()
        mock_box_response.status_code = 200
        mock_box_response.ok = True
        return mock_box_response, items[offset:limit + offset]
    return get_response


def _assert_collaborator_added(test_folder, collaborator, mock_box_session, mock_collab_response, notify, role, data):
    mock_box_session.post.return_value = mock_collab_response
    collaboration = test_folder.add_collaborator(collaborator, role, notify)
    assert isinstance(collaboration, Collaboration)
    expected_url = API.BASE_API_URL + '/collaborations'
    params = {'notify': notify}
    mock_box_session.post.assert_called_once_with(expected_url, expect_json_response=True, data=data, params=params)


@pytest.mark.parametrize('notify', [True, False])
@pytest.mark.parametrize('role', iter(CollaborationRole))
def test_add_user_collaborator(test_folder, mock_user, mock_box_session, mock_collab_response, notify, role):
    data = json.dumps({
        'item': {'type': 'folder', 'id': test_folder.object_id},
        'accessible_by': {'id': mock_user.object_id, 'type': 'user'},
        'role': role,
    })
    _assert_collaborator_added(test_folder, mock_user, mock_box_session, mock_collab_response, notify, role, data)


@pytest.mark.parametrize('notify', [True, False])
@pytest.mark.parametrize('role', iter(CollaborationRole))
def test_add_group_collaborator(test_folder, mock_group, mock_box_session, mock_collab_response, notify, role):
    data = json.dumps({
        'item': {'type': 'folder', 'id': test_folder.object_id},
        'accessible_by': {'id': mock_group.object_id, 'type': 'group'},
        'role': role,
    })
    _assert_collaborator_added(test_folder, mock_group, mock_box_session, mock_collab_response, notify, role, data)


@pytest.mark.parametrize('notify', [True, False])
@pytest.mark.parametrize('role', iter(CollaborationRole))
def test_add_email_collaborator(test_folder, mock_box_session, mock_collab_response, notify, role):
    email_address = 'foo@example.com'
    data = json.dumps({
        'item': {'type': 'folder', 'id': test_folder.object_id},
        'accessible_by': {'login': email_address, 'type': 'user'},
        'role': role,
    })
    _assert_collaborator_added(test_folder, email_address, mock_box_session, mock_collab_response, notify, role, data)


def test_add_collaborator_raises_for_bad_type(test_folder):
    with pytest.raises(TypeError):
        test_folder.add_collaborator(b'byte string', CollaborationRole.EDITOR)


@pytest.mark.parametrize('recursive', [True, False])
def test_delete_folder(test_folder, mock_box_session, recursive, etag, if_match_header):
    test_folder.delete(recursive=recursive, etag=etag)
    expected_url = test_folder.get_url()
    mock_box_session.delete.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params={'recursive': recursive},
        headers=if_match_header,
    )


@pytest.mark.parametrize('limit,offset,fields', [(1, 0, None), (100, 0, ['foo', 'bar']), (1, 1, None)])
def test_get_items(test_folder, mock_box_session, mock_items_response, limit, offset, fields):
    # pylint:disable=redefined-outer-name
    expected_url = test_folder.get_url('items')
    mock_box_session.get.return_value, expected_items = mock_items_response(limit, offset)
    items = test_folder.get_items(limit, offset, fields)
    expected_params = {'limit': limit, 'offset': offset}
    if fields:
        expected_params['fields'] = ','.join(fields)
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert items == expected_items
    assert all([i.id == e.object_id for i, e in zip(items, expected_items)])


@pytest.mark.parametrize('is_stream', (True, False))
def test_upload(
        test_folder,
        mock_box_session,
        mock_content_response,
        mock_upload_response,
        mock_file_path,
        mock_object_id,
        is_stream,
):
    expected_url = '{0}/files/content'.format(API.UPLOAD_URL)
    mock_box_session.post.return_value = mock_upload_response
    if is_stream:
        mock_file_stream = BytesIO(mock_content_response.content)
        new_file = test_folder.upload_stream(mock_file_stream, basename(mock_file_path))
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        mock_file_stream = mock_file.return_value
        with patch('boxsdk.object.folder.open', mock_file, create=True):
            new_file = test_folder.upload(mock_file_path)
    mock_files = {'file': ('unused', mock_file_stream)}
    data = {'attributes': json.dumps({'name': basename(mock_file_path), 'parent': {'id': mock_object_id}})}
    mock_box_session.post.assert_called_once_with(expected_url, expect_json_response=False, files=mock_files, data=data)
    assert isinstance(new_file, File)
    assert new_file.object_id == mock_upload_response.json()['entries'][0]['id']


def test_create_subfolder(test_folder, mock_box_session, mock_object_id, mock_folder_response):
    expected_url = test_folder.get_type_url()
    mock_box_session.post.return_value = mock_folder_response
    new_folder = test_folder.create_subfolder('name')
    data = json.dumps({'name': 'name', 'parent': {'id': mock_object_id}})
    mock_box_session.post.assert_called_once_with(expected_url, data=data)
    assert isinstance(new_folder, Folder)
    assert new_folder.object_id == mock_object_id


@pytest.mark.parametrize('sync_state', iter(FolderSyncState))
def test_update_sync_state(test_folder, mock_folder_response, mock_box_session, sync_state):
    expected_url = test_folder.get_url()
    mock_box_session.put.return_value = mock_folder_response
    data = {'sync_state': sync_state}
    update_response = test_folder.update_sync_state(sync_state)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), params=None, headers=None)
    assert isinstance(update_response, Folder)
    assert update_response.object_id == test_folder.object_id
