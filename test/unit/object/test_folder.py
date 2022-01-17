# coding: utf-8

import json
from io import BytesIO
from os.path import basename
from mock import mock_open, patch, Mock, MagicMock
import pytest
from boxsdk.config import API
from boxsdk.exception import BoxAPIException
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.enterprise import Enterprise
from boxsdk.object.file import File
from boxsdk.object.metadata_cascade_policy import MetadataCascadePolicy
from boxsdk.object.web_link import WebLink
from boxsdk.object.collaboration import Collaboration, CollaborationRole
from boxsdk.object.folder import Folder, FolderSyncState
from boxsdk.object.upload_session import UploadSession
from boxsdk.session.box_response import BoxResponse
from boxsdk.util.chunked_uploader import ChunkedUploader


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
        entries = items_json[offset:limit + offset]
        mock_box_response = Mock(BoxResponse)
        mock_network_response = Mock(DefaultNetworkResponse)
        mock_box_response.network_response = mock_network_response
        mock_box_response.json.return_value = mock_json = {
            'entries': entries,
            'total_count': len(entries),
            'limit': limit,
            'offset': offset,
        }
        mock_box_response.content = json.dumps(mock_json).encode()
        mock_box_response.status_code = 200
        mock_box_response.ok = True
        return mock_box_response, items[offset:limit + offset]
    return get_response


def test_get_chunked_uploader(mock_box_session, mock_content_response, mock_file_path, test_folder):
    expected_url = f'{API.UPLOAD_URL}/files/upload_sessions'
    mock_file_stream = BytesIO(mock_content_response.content)
    file_size = 197520
    file_name = 'file'
    part_size = 12345
    total_parts = 16
    num_parts_processed = 0
    upload_session_type = 'upload_session'
    upload_session_id = 'F971964745A5CD0C001BBE4E58196BFD'
    expected_data = {
        'folder_id': test_folder.object_id,
        'file_size': file_size,
        'file_name': file_name,
    }
    mock_box_session.post.return_value.json.return_value = {
        'id': upload_session_id,
        'type': upload_session_type,
        'num_parts_processed': num_parts_processed,
        'total_parts': total_parts,
        'part_size': part_size,
    }
    with patch('os.stat') as stat:
        stat.return_value.st_size = file_size
        with patch('boxsdk.object.folder.open', return_value=mock_file_stream):
            chunked_uploader = test_folder.get_chunked_uploader(mock_file_path)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    upload_session = chunked_uploader._upload_session
    assert upload_session.part_size == part_size
    assert upload_session.total_parts == total_parts
    assert upload_session.num_parts_processed == num_parts_processed
    assert upload_session.type == upload_session_type
    assert upload_session.id == upload_session_id
    assert isinstance(chunked_uploader, ChunkedUploader)


@pytest.fixture()
def mock_items_response_with_marker(mock_items):
    # pylint:disable=redefined-outer-name
    def get_response(limit, offset):
        items_json, items = mock_items
        entries = items_json[offset:limit + offset]
        mock_box_response = Mock(BoxResponse)
        mock_network_response = Mock(DefaultNetworkResponse)
        mock_box_response.network_response = mock_network_response
        mock_box_response.json.return_value = mock_json = {
            'entries': entries,
            'total_count': len(entries),
            'limit': limit,
            'offset': offset,
        }
        mock_box_response.content = json.dumps(mock_json).encode()
        mock_box_response.status_code = 200
        mock_box_response.ok = True
        return mock_box_response, items[offset:limit + offset]
    return get_response


def _assert_collaborator_added(test_folder, collaborator, mock_box_session, mock_collab_response, notify, role, can_view_path, data):
    mock_box_session.post.return_value = mock_collab_response
    collaboration = test_folder.add_collaborator(collaborator, role, notify, can_view_path)
    assert isinstance(collaboration, Collaboration)
    expected_url = API.BASE_API_URL + '/collaborations'
    params = {'notify': notify}
    mock_box_session.post.assert_called_once_with(expected_url, expect_json_response=True, data=data, params=params)


@pytest.mark.parametrize('accessible_by', ['user', 'group', 'email'])
@pytest.mark.parametrize('notify', [True, False])
@pytest.mark.parametrize('role', iter(CollaborationRole))
@pytest.mark.parametrize('can_view_path', [True, False])
def test_add_collaborator(test_folder, mock_user, mock_group, mock_box_session, mock_collab_response, accessible_by, notify, role, can_view_path):
    accessible_dict = {
        'user': (mock_user, {'id': mock_user.object_id, 'type': 'user'}),
        'group': (mock_group, {'id': mock_group.object_id, 'type': 'group'}),
        'email': ('foo@example.com', {'login': 'foo@example.com', 'type': 'user'}),
    }

    invitee, mock_accessible_by = accessible_dict[accessible_by]

    body_params = {
        'item': {'id': test_folder.object_id, 'type': 'folder'},
        'accessible_by': mock_accessible_by,
        'role': role,
    }
    if can_view_path:
        body_params['can_view_path'] = True
    data = json.dumps(body_params)
    _assert_collaborator_added(test_folder, invitee, mock_box_session, mock_collab_response, notify, role, can_view_path, data)


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


@pytest.mark.parametrize('limit,offset,fields,sort,direction', [
    (1, 0, None, None, None),
    (100, 0, ['foo', 'bar'], None, None),
    (1, 1, None, None, None),
    (1, 0, None, 'name', 'ASC'),
    (1, 1, None, 'date', 'DESC')
])
def test_get_items(test_folder, mock_box_session, mock_items_response, limit, offset, fields, sort, direction):
    # pylint:disable=redefined-outer-name
    expected_url = test_folder.get_url('items')
    mock_box_session.get.return_value, expected_items = mock_items_response(limit, offset)
    items = test_folder.get_items(limit, offset, fields=fields, sort=sort, direction=direction)
    expected_params = {'limit': limit, 'offset': offset}
    if fields:
        expected_params['fields'] = ','.join(fields)
    if sort:
        expected_params['sort'] = sort
    if direction:
        expected_params['direction'] = direction
    for actual, expected in zip(items, expected_items):
        assert actual == expected
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert all(i.id == e.object_id for (i, e) in zip(items, expected_items))


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
        etag,
        sha1,
        if_match_sha1_header,
):
    # pylint:disable=too-many-locals
    file_description = 'Test File Description'
    content_created_at = '1970-01-01T00:00:00+00:00'
    content_modified_at = '1970-01-01T11:11:11+11:11'
    additional_attributes = {'attr': 123}
    expected_url = f'{API.UPLOAD_URL}/files/content'
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
            file_description,
            upload_using_accelerator=upload_using_accelerator,
            content_created_at=content_created_at,
            content_modified_at=content_modified_at,
            additional_attributes=additional_attributes,
            sha1=sha1,
            etag=etag,
        )
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        mock_file_stream = mock_file.return_value
        with patch('boxsdk.object.folder.open', mock_file, create=True):
            new_file = test_folder.upload(
                mock_file_path,
                file_description=file_description,
                upload_using_accelerator=upload_using_accelerator,
                content_created_at=content_created_at,
                content_modified_at=content_modified_at,
                additional_attributes=additional_attributes,
                sha1=sha1,
                etag=etag,
            )

    mock_files = {'file': ('unused', mock_file_stream)}
    attributes = {
        'name': basename(mock_file_path),
        'parent': {'id': mock_object_id},
        'description': file_description,
        'content_created_at': content_created_at,
        'content_modified_at': content_modified_at,
    }
    # Using `update` to mirror the actual impl, since the attributes could otherwise come through in a different order
    # in Python 2 tests
    attributes.update(additional_attributes)
    data = {'attributes': json.dumps(attributes)}
    mock_box_session.post.assert_called_once_with(expected_url, expect_json_response=False, files=mock_files, data=data, headers=if_match_sha1_header)
    assert isinstance(new_file, File)
    assert new_file.object_id == mock_object_id
    assert 'id' in new_file
    assert new_file['id'] == mock_object_id
    assert new_file.description == file_description
    assert not hasattr(new_file, 'entries')
    assert 'entries' not in new_file


@pytest.mark.parametrize('is_stream', (True, False))
def test_upload_combines_preflight_and_accelerator_calls_if_both_are_requested(
        test_folder,
        mock_box_session,
        mock_file_path,
        mock_content_response,
        mock_accelerator_response_for_new_uploads,
        is_stream
):
    mock_box_session.options.return_value = mock_accelerator_response_for_new_uploads

    if is_stream:
        mock_file_stream = BytesIO(mock_content_response.content)
        test_folder.upload_stream(
            mock_file_stream,
            basename(mock_file_path),
            preflight_check=True,
            upload_using_accelerator=True,
        )
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        with patch('boxsdk.object.folder.open', mock_file, create=True):
            test_folder.upload(
                mock_file_path,
                preflight_check=True,
                upload_using_accelerator=True,
            )

    mock_box_session.options.assert_called_once()


def test_create_upload_session(test_folder, mock_box_session):
    expected_url = f'{API.UPLOAD_URL}/files/upload_sessions'
    file_size = 197520
    file_name = 'test_file.pdf'
    upload_session_id = 'F971964745A5CD0C001BBE4E58196BFD'
    upload_session_type = 'upload_session'
    num_parts_processed = 0
    total_parts = 16
    part_size = 12345
    expected_data = {
        'folder_id': test_folder.object_id,
        'file_size': file_size,
        'file_name': file_name,
    }
    mock_box_session.post.return_value.json.return_value = {
        'id': upload_session_id,
        'type': upload_session_type,
        'num_parts_processed': num_parts_processed,
        'total_parts': total_parts,
        'part_size': part_size,
    }
    upload_session = test_folder.create_upload_session(file_size, file_name)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert isinstance(upload_session, UploadSession)
    assert upload_session.part_size == part_size
    assert upload_session.total_parts == total_parts
    assert upload_session.num_parts_processed == num_parts_processed
    assert upload_session.type == upload_session_type
    assert upload_session.id == upload_session_id


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


def test_preflight(
        test_folder,
        mock_object_id,
        mock_box_session,
        mock_accelerator_response_for_new_uploads,
        mock_new_upload_accelerator_url,
):
    new_file_size, new_file_name = 100, 'foo.txt'
    mock_box_session.options.return_value = mock_accelerator_response_for_new_uploads

    accelerator_url = test_folder.preflight_check(size=new_file_size, name=new_file_name)

    mock_box_session.options.assert_called_once_with(
        url=f'{API.BASE_API_URL}/files/content',
        expect_json_response=True,
        data=json.dumps(
            {
                'size': new_file_size,
                'name': new_file_name,
                'parent': {'id': mock_object_id},
            }
        ),
    )
    assert accelerator_url == mock_new_upload_accelerator_url


def test_create_web_link_returns_the_correct_web_link_object(test_folder, mock_box_session):
    expected_url = f"{API.BASE_API_URL}/web_links"
    expected_name = 'Test WebLink'
    description = 'Test Description'
    test_web_link_url = 'https://test.com'
    mock_box_session.post.return_value.json.return_value = {
        'type': 'web_link',
        'id': '42',
        'url': test_web_link_url,
        'name': expected_name,
        'description': description
    }
    new_web_link = test_folder.create_web_link(test_web_link_url, expected_name, description)
    data = {
        'url': test_web_link_url,
        'parent': {
            'id': '42',
        },
        'name': expected_name,
        'description': description,
    }
    mock_box_session.post.assert_called_once_with(
        expected_url,
        data=json.dumps(data),
    )
    assert isinstance(new_web_link, WebLink)
    assert new_web_link.object_id == '42'
    assert new_web_link.url == test_web_link_url
    assert new_web_link.name == expected_name
    assert new_web_link.description == description


def test_get_metadata_cascade_policies(test_folder, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/metadata_cascade_policies'
    params = {'folder_id': test_folder.object_id}
    mock_box_session.get.return_value.json.return_value = {
        'entries': [
            {
                'id': '84113349-794d-445c-b93c-d8481b223434',
                'type': 'metadata_cascade_policy',
                'parent': {
                    'type': 'folder',
                    'id': test_folder.object_id,
                },
                'scope': 'enterprise_11111',
                'templateKey': 'testTemplate',
            }
        ],
        'next_marker': None,
        'prev_marker': None,
    }

    cascade_policies = test_folder.get_metadata_cascade_policies()
    policy = cascade_policies.next()

    mock_box_session.get.assert_called_once_with(expected_url, params=params)
    assert isinstance(policy, MetadataCascadePolicy)
    assert policy.object_id == '84113349-794d-445c-b93c-d8481b223434'
    assert policy.scope == 'enterprise_11111'
    assert policy.templateKey == 'testTemplate'
    # pylint: disable=protected-access
    assert policy._session == mock_box_session


def test_cascade_metadata(test_folder, mock_box_session, test_metadata_template):
    expected_url = f'{API.BASE_API_URL}/metadata_cascade_policies'
    expected_body = {
        'folder_id': test_folder.object_id,
        'scope': test_metadata_template.scope,
        'templateKey': test_metadata_template.template_key,
    }
    mock_box_session.post.return_value.json.return_value = {
        'id': '84113349-794d-445c-b93c-d8481b223434',
        'type': 'metadata_cascade_policy',
        'owner_enterprise': {
            'type': 'enterprise',
            'id': '11111',
        },
        'parent': {
            'type': 'folder',
            'id': test_folder.object_id,
        },
        'scope': test_metadata_template.scope,
        'templateKey': test_metadata_template.template_key,
    }

    cascade_policy = test_folder.cascade_metadata(test_metadata_template)

    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(cascade_policy, MetadataCascadePolicy)
    assert cascade_policy.object_id == '84113349-794d-445c-b93c-d8481b223434'
    enterprise = cascade_policy.owner_enterprise
    assert isinstance(enterprise, Enterprise)
    assert enterprise.object_id == '11111'
    folder = cascade_policy.parent
    assert isinstance(folder, Folder)
    assert folder.object_id == test_folder.object_id
    assert cascade_policy.scope == test_metadata_template.scope
    assert cascade_policy.templateKey == test_metadata_template.template_key


def test_get_folder_locks(test_folder, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/folder_locks'
    params = {'folder_id': test_folder.object_id}
    mock_box_session.get.return_value.json.return_value = {
        "entries": [
            {
                "folder": {
                    "id": "12345",
                    "etag": "1",
                    "type": "folder",
                    "sequence_id": "3",
                    "name": "Contracts"
                },
                "id": "12345678",
                "type": "folder_lock",
                "created_by": {
                    "id": "11446498",
                    "type": "user"
                },
                "created_at": "2020-09-14T23:12:53Z",
                "locked_operations": {
                    "move": True,
                    "delete": True
                },
                "lock_type": "freeze"
            }
        ],
        "limit": 1000,
        "next_marker": None
    }

    folder_locks = test_folder.get_locks()
    lock = folder_locks.next()

    mock_box_session.get.assert_called_once_with(expected_url, params=params)
    assert lock.id == '12345678'
    assert lock.folder.id == '12345'
    assert lock.locked_operations['move']
    # pylint: disable=protected-access
    assert lock._session == mock_box_session


def test_create_folder_lock(test_folder, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/folder_locks'
    expected_body = {
        "folder": {
            "type": "folder",
            "id": test_folder.object_id
        },
        "locked_operations": {
            "move": True,
            "delete": True
        }
    }
    mock_box_session.post.return_value.json.return_value = {
        "id": "12345678",
        "type": "folder_lock",
        "created_at": "2020-09-14T23:12:53Z",
        "created_by": {
            "id": "11446498",
            "type": "user"
        },
        "folder": {
            "id": "12345",
            "type": "folder",
            "etag": "1",
            "name": "Contracts",
            "sequence_id": "3"
        },
        "lock_type": "freeze",
        "locked_operations": {
            "delete": True,
            "move": True
        }
    }

    lock = test_folder.create_lock()

    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert lock.id == '12345678'
    assert lock.folder.id == '12345'
    assert lock.locked_operations['move']
    # pylint: disable=protected-access
    assert lock._session == mock_box_session


def test_delete_folder_lock(test_folder_lock, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/folder_locks/{test_folder_lock.object_id}'
    test_folder_lock.delete()
    mock_box_session.delete.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        headers=None,
        params={}
    )
