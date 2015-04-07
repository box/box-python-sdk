# coding: utf-8

from __future__ import unicode_literals
import json
from os.path import basename
from mock import mock_open, patch, Mock, MagicMock
import pytest
from six import BytesIO
from six.moves import zip  # pylint:disable=redefined-builtin,import-error
from boxsdk.config import API
from boxsdk.exception import BoxAPIException
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.file import File
from boxsdk.object.collaboration import Collaboration, CollaborationRole
from boxsdk.object.folder import Folder, FolderSyncState
from boxsdk.session.box_session import BoxResponse


# pylint:disable=protected-access
# pylint:disable=redefined-outer-name


@pytest.fixture()
def mock_new_upload_accelerator_url():
    return 'https://upload.box.com/api/2.0/files/content?upload_session_id=123'


@pytest.fixture(scope='function')
def mock_accelerator_response_for_new_uploads(make_mock_box_request, mock_new_upload_accelerator_url):
    mock_response, _ = make_mock_box_request(
        response={
            'upload_url': mock_new_upload_accelerator_url,
            'upload_token': None,
        }
    )
    return mock_response


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
        'item': {'id': test_folder.object_id, 'type': 'folder'},
        'accessible_by': {'id': mock_user.object_id, 'type': 'user'},
        'role': role,
    })
    _assert_collaborator_added(test_folder, mock_user, mock_box_session, mock_collab_response, notify, role, data)


@pytest.mark.parametrize('notify', [True, False])
@pytest.mark.parametrize('role', iter(CollaborationRole))
def test_add_group_collaborator(test_folder, mock_group, mock_box_session, mock_collab_response, notify, role):
    data = json.dumps({
        'item': {'id': test_folder.object_id, 'type': 'folder'},
        'accessible_by': {'id': mock_group.object_id, 'type': 'group'},
        'role': role,
    })
    _assert_collaborator_added(test_folder, mock_group, mock_box_session, mock_collab_response, notify, role, data)


@pytest.mark.parametrize('notify', [True, False])
@pytest.mark.parametrize('role', iter(CollaborationRole))
def test_add_email_collaborator(test_folder, mock_box_session, mock_collab_response, notify, role):
    email_address = 'foo@example.com'
    data = json.dumps({
        'item': {'id': test_folder.object_id, 'type': 'folder'},
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
        upload_using_accelerator,
        mock_accelerator_response_for_new_uploads,
        mock_new_upload_accelerator_url,
        upload_using_accelerator_fails,
        is_stream,
):
    expected_url = '{0}/files/content'.format(API.UPLOAD_URL)
    if upload_using_accelerator:
        if upload_using_accelerator_fails:
            mock_box_session.options.side_effect = BoxAPIException(400)
        else:
            mock_box_session.options.return_value = mock_accelerator_response_for_new_uploads
            expected_url = mock_new_upload_accelerator_url

    mock_box_session.post.return_value = mock_upload_response

    if is_stream:
        mock_file_stream = BytesIO(mock_content_response.content)
        new_file = test_folder.upload_stream(
            mock_file_stream,
            basename(mock_file_path),
            upload_using_accelerator=upload_using_accelerator,
        )
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        mock_file_stream = mock_file.return_value
        with patch('boxsdk.object.folder.open', mock_file, create=True):
            new_file = test_folder.upload(
                mock_file_path,
                upload_using_accelerator=upload_using_accelerator,
            )

    mock_files = {'file': ('unused', mock_file_stream)}
    data = {'attributes': json.dumps({'name': basename(mock_file_path), 'parent': {'id': mock_object_id}})}
    mock_box_session.post.assert_called_once_with(expected_url, expect_json_response=False, files=mock_files, data=data)
    assert isinstance(new_file, File)
    assert new_file.object_id == mock_upload_response.json()['entries'][0]['id']


def test_upload_stream_does_preflight_check_if_specified(
        mock_box_session,
        test_folder,
        preflight_check,
        preflight_fails,
        file_size,
):
    with patch.object(Folder, 'preflight_check', return_value=None):
        kwargs = {'file_stream': BytesIO(b'some bytes'), 'file_name': 'foo.txt'}
        mock_box_session.post = MagicMock()
        if preflight_check:
            kwargs['preflight_check'] = preflight_check
            kwargs['preflight_expected_size'] = file_size
        if preflight_fails:
            test_folder.preflight_check.side_effect = BoxAPIException(400)
            with pytest.raises(BoxAPIException):
                test_folder.upload_stream(**kwargs)
        else:
            test_folder.upload_stream(**kwargs)

        if preflight_check:
            assert test_folder.preflight_check.called_once_with(size=file_size, name='foo.txt')
            _assert_post_called_correctly(mock_box_session, preflight_fails)
        else:
            assert not test_folder.preflight_check.called


def _assert_post_called_correctly(mock_box_session, preflight_fails):
    if preflight_fails:
        assert not mock_box_session.post.called
    else:
        assert mock_box_session.post.called


@patch('boxsdk.object.folder.open', mock_open(read_data=b'some bytes'), create=True)
def test_upload_does_preflight_check_if_specified(
        mock_box_session,
        test_folder,
        mock_file_path,
        preflight_check,
        preflight_fails,
        file_size,
):
    with patch.object(Folder, 'preflight_check', return_value=None):
        kwargs = {'file_path': mock_file_path, 'file_name': 'foo.txt'}
        mock_box_session.post = MagicMock()
        if preflight_check:
            kwargs['preflight_check'] = preflight_check
            kwargs['preflight_expected_size'] = file_size
        if preflight_fails:
            test_folder.preflight_check.side_effect = BoxAPIException(400)
            with pytest.raises(BoxAPIException):
                test_folder.upload(**kwargs)
        else:
            test_folder.upload(**kwargs)

        if preflight_check:
            assert test_folder.preflight_check.called_once_with(size=file_size, name='foo.txt')
            _assert_post_called_correctly(mock_box_session, preflight_fails)
        else:
            assert not test_folder.preflight_check.called


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


def test_preflight(test_folder, mock_object_id, mock_box_session):
    new_file_size, new_file_name = 100, 'foo.txt'
    test_folder.preflight_check(size=new_file_size, name=new_file_name)
    mock_box_session.options.assert_called_once_with(
        url='{0}/files/content'.format(API.BASE_API_URL),
        expect_json_response=False,
        data=json.dumps(
            {
                'size': new_file_size,
                'name': new_file_name,
                'parent': {'id': mock_object_id},
            }
        ),
    )
