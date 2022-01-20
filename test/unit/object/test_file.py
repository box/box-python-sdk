# coding: utf-8

import json
from io import BytesIO

from mock import mock_open, patch, Mock
import pytest
from boxsdk.config import API
from boxsdk.exception import BoxAPIException
from boxsdk.object.comment import Comment
from boxsdk.object.file import File
from boxsdk.object.file_version import FileVersion
from boxsdk.object.task import Task
from boxsdk.object.upload_session import UploadSession
from boxsdk.util.chunked_uploader import ChunkedUploader
from boxsdk.util.default_arg_value import SDK_VALUE_NOT_SET


# pylint:disable=protected-access
# pylint:disable=redefined-outer-name

@pytest.fixture()
def mock_accelerator_upload_url_for_update():
    return 'https://upload.box.com/api/2.0/files/fake_file_id/content?upload_session_id=123'


@pytest.fixture(scope='function')
def mock_accelerator_response_for_update(make_mock_box_request, mock_accelerator_upload_url_for_update):
    mock_response, _ = make_mock_box_request(
        response={
            'upload_url': mock_accelerator_upload_url_for_update,
            'download_url': None,
        }
    )
    return mock_response


def test_delete_file(test_file, mock_box_session, etag, if_match_header):
    test_file.delete(etag=etag)
    expected_url = test_file.get_url()
    mock_box_session.delete.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params={},
        headers=if_match_header,
    )


def test_create_upload_session(test_file, mock_box_session):
    expected_url = f'{API.UPLOAD_URL}/files/{test_file.object_id}/upload_sessions'
    file_size = 197520
    part_size = 12345
    total_parts = 16
    num_parts_processed = 0
    upload_session_type = 'upload_session'
    upload_session_id = 'F971964745A5CD0C001BBE4E58196BFD'
    file_name = 'test_file.pdf'
    expected_data = {
        'file_id': test_file.object_id,
        'file_size': file_size,
        'file_name': file_name
    }
    mock_box_session.post.return_value.json.return_value = {
        'id': upload_session_id,
        'type': upload_session_type,
        'num_parts_processed': num_parts_processed,
        'total_parts': total_parts,
        'part_size': part_size,
    }
    upload_session = test_file.create_upload_session(file_size, file_name)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert isinstance(upload_session, UploadSession)
    assert upload_session._session == mock_box_session
    assert upload_session.part_size == part_size
    assert upload_session.total_parts == total_parts
    assert upload_session.num_parts_processed == num_parts_processed
    assert upload_session.type == upload_session_type
    assert upload_session.id == upload_session_id


def test_get_chunked_uploader(mock_box_session, mock_content_response, mock_file_path, test_file):
    expected_url = f'{API.UPLOAD_URL}/files/{test_file.object_id}/upload_sessions'
    mock_file_stream = BytesIO(mock_content_response.content)
    file_size = 197520
    part_size = 12345
    total_parts = 16
    num_parts_processed = 0
    upload_session_type = 'upload_session'
    upload_session_id = 'F971964745A5CD0C001BBE4E58196BFD'
    expected_data = {
        'file_id': test_file.object_id,
        'file_size': file_size,
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
        with patch('boxsdk.object.file.open', return_value=mock_file_stream):
            chunked_uploader = test_file.get_chunked_uploader(mock_file_path)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    upload_session = chunked_uploader._upload_session
    assert upload_session.part_size == part_size
    assert upload_session.total_parts == total_parts
    assert upload_session.num_parts_processed == num_parts_processed
    assert upload_session.type == upload_session_type
    assert upload_session.id == upload_session_id
    assert isinstance(chunked_uploader, ChunkedUploader)


def test_create_task(test_file, test_task, mock_box_session):
    # pylint:disable=redefined-outer-name
    expected_url = f"{API.BASE_API_URL}/tasks"
    due_at = '2014-04-03T11:09:43-07:00'
    action = 'review'
    message = 'Test Message'
    expected_body = {
        'item': {
            'type': 'file',
            'id': '42',
        },
        'action': action,
        'message': message,
        'due_at': due_at,
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': test_task.object_type,
        'id': test_task.object_id,
        'due_at': due_at,
        'action': action,
        'message': message,
    }
    value = json.dumps(expected_body)
    new_task = test_file.create_task(message=message, due_at=due_at)
    mock_box_session.post.assert_called_once_with(expected_url, data=value)
    assert isinstance(new_task, Task)
    assert new_task.object_type == test_task.object_type
    assert new_task.object_id == test_task.object_id
    assert new_task.action == action
    assert new_task.message == message
    assert new_task.due_at == due_at


def test_create_task_with_review(test_file, test_task, mock_box_session):
    # pylint:disable=redefined-outer-name
    expected_url = f"{API.BASE_API_URL}/tasks"
    due_at = '2020-09-18T12:09:43-00:00'
    action = 'complete'
    message = 'Test Message'
    completion_rule = 'any_assignee'
    expected_body = {
        'item': {
            'type': 'file',
            'id': '42',
        },
        'action': action,
        'message': message,
        'due_at': due_at,
        'completion_rule': completion_rule,
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': test_task.object_type,
        'id': test_task.object_id,
        'due_at': due_at,
        'action': action,
        'message': message,
        'completion_rule': completion_rule,
    }
    value = json.dumps(expected_body)
    new_task = test_file.create_task(
        message=message,
        due_at=due_at,
        action=action,
        completion_rule=completion_rule,
    )
    mock_box_session.post.assert_called_once_with(expected_url, data=value)
    assert isinstance(new_task, Task)
    assert new_task.object_type == test_task.object_type
    assert new_task.object_id == test_task.object_id
    assert new_task.action == action
    assert new_task.message == message
    assert new_task.due_at == due_at
    assert new_task.completion_rule == completion_rule


def test_get_tasks(test_file, mock_box_session):
    expected_url = test_file.get_url('tasks')
    task_body = {
        'type': 'task',
        'id': '12345',
        'item': {
            'type': 'file',
            'id': '33333',
        },
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [task_body],
    }
    tasks = test_file.get_tasks()
    task = tasks.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(task, Task)
    assert task.id == task_body['id']
    assert task.object_type == task_body['type']
    assert task.item['id'] == task_body['item']['id']


def test_get_download_url(test_file, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/content'
    download_url = 'https://dl.boxcloud.com/sdjhfgksdjfgshdbg'
    mock_box_session.get.return_value.headers = {
        'location': download_url
    }
    url = test_file.get_download_url()
    mock_box_session.get.assert_called_once_with(
        expected_url,
        params=None,
        expect_json_response=False,
        allow_redirects=False
    )
    assert url == download_url


def test_get_download_url_file_version(test_file, test_file_version, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/content'
    download_url = 'https://dl.boxcloud.com/sdjhfgksdjfgshdbg'
    mock_box_session.get.return_value.headers = {
        'location': download_url
    }
    url = test_file.get_download_url(file_version=test_file_version)
    mock_box_session.get.assert_called_once_with(
        expected_url,
        params={'version': test_file_version.object_id},
        expect_json_response=False,
        allow_redirects=False
    )
    assert url == download_url


@pytest.mark.parametrize('params,expected_query,expected_headers', [
    ({}, None, None),
    ({'byte_range': (100, 199)}, None, {'Range': 'bytes=100-199'}),
    ({'byte_range': (100,)}, None, {'Range': 'bytes=100-'}),
])
def test_download_to(test_file, mock_box_session, mock_content_response, params, expected_query, expected_headers):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/content'
    mock_box_session.get.return_value = mock_content_response
    mock_writeable_stream = BytesIO()
    test_file.download_to(mock_writeable_stream, **params)
    mock_writeable_stream.seek(0)
    assert mock_writeable_stream.read() == mock_content_response.content
    mock_box_session.get.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        stream=True,
        params=expected_query,
        headers=expected_headers
    )


def test_download_to_file_version(test_file, test_file_version, mock_box_session, mock_content_response):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/content'
    mock_box_session.get.return_value = mock_content_response
    mock_writeable_stream = BytesIO()
    test_file.download_to(mock_writeable_stream, file_version=test_file_version)
    mock_writeable_stream.seek(0)
    assert mock_writeable_stream.read() == mock_content_response.content
    mock_box_session.get.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        stream=True,
        headers=None,
        params={'version': test_file_version.object_id}
    )


@pytest.mark.parametrize('params,expected_query,expected_headers', [
    ({}, None, None),
    ({'byte_range': (100, 199)}, None, {'Range': 'bytes=100-199'}),
])
def test_get_content(test_file, mock_box_session, mock_content_response, params, expected_query, expected_headers):
    expected_url = test_file.get_url('content')
    mock_box_session.get.return_value = mock_content_response
    file_content = test_file.content(**params)
    assert file_content == mock_content_response.content
    mock_box_session.get.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params=expected_query,
        headers=expected_headers
    )


def test_get_content_file_version(test_file, mock_box_session, mock_content_response, test_file_version):
    expected_url = test_file.get_url('content')
    mock_box_session.get.return_value = mock_content_response
    file_content = test_file.content(file_version=test_file_version)
    assert file_content == mock_content_response.content
    mock_box_session.get.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params={'version': test_file_version.object_id},
        headers=None
    )


@pytest.mark.parametrize('is_stream', (True, False))
def test_update_contents(
        test_file,
        mock_box_session,
        mock_content_response,
        mock_upload_response,
        mock_file_path,
        etag,
        sha1,
        upload_using_accelerator,
        mock_accelerator_response_for_update,
        mock_accelerator_upload_url_for_update,
        upload_using_accelerator_fails,
        if_match_sha1_header,
        is_stream,
):
    # pylint:disable=too-many-locals
    file_new_name = 'new_file_name'
    content_modified_at = '1970-01-01T11:11:11+11:11'
    additional_attributes = {'attr': 123}
    expected_url = test_file.get_url('content').replace(API.BASE_API_URL, API.UPLOAD_URL)
    if upload_using_accelerator:
        if upload_using_accelerator_fails:
            mock_box_session.options.side_effect = BoxAPIException(400)
        else:
            mock_box_session.options.return_value = mock_accelerator_response_for_update
            expected_url = mock_accelerator_upload_url_for_update

    mock_box_session.post.return_value = mock_upload_response

    if is_stream:
        mock_file_stream = BytesIO(mock_content_response.content)
        new_file = test_file.update_contents_with_stream(
            mock_file_stream,
            etag=etag,
            upload_using_accelerator=upload_using_accelerator,
            file_name=file_new_name,
            content_modified_at=content_modified_at,
            additional_attributes=additional_attributes,
            sha1=sha1,
        )
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        mock_file_stream = mock_file.return_value
        with patch('boxsdk.object.file.open', mock_file, create=True):
            new_file = test_file.update_contents(
                mock_file_path,
                etag=etag,
                upload_using_accelerator=upload_using_accelerator,
                file_name=file_new_name,
                content_modified_at=content_modified_at,
                additional_attributes=additional_attributes,
                sha1=sha1,
            )

    mock_files = {'file': ('unused', mock_file_stream)}
    attributes = {
        'name': file_new_name,
        'content_modified_at': content_modified_at,
    }
    # Using `update` to mirror the actual impl, since the attributes could otherwise come through in a different order
    # in Python 2 tests
    attributes.update(additional_attributes)
    data = {'attributes': json.dumps(attributes)}
    mock_box_session.post.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        files=mock_files,
        data=data,
        headers=if_match_sha1_header,
    )
    assert isinstance(new_file, File)
    assert new_file.object_id == test_file.object_id
    assert 'id' in new_file
    assert new_file['id'] == test_file.object_id
    assert not hasattr(new_file, 'entries')
    assert 'entries' not in new_file


@pytest.mark.parametrize('is_stream', (True, False))
def test_update_contents_combines_preflight_and_accelerator_calls_if_both_are_requested(
        test_file,
        mock_box_session,
        mock_file_path,
        mock_content_response,
        mock_accelerator_response_for_update,
        is_stream
):
    mock_box_session.options.return_value = mock_accelerator_response_for_update

    if is_stream:
        mock_file_stream = BytesIO(mock_content_response.content)
        test_file.update_contents_with_stream(
            mock_file_stream,
            preflight_check=True,
            upload_using_accelerator=True,
        )
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        with patch('boxsdk.object.file.open', mock_file, create=True):
            test_file.update_contents(
                mock_file_path,
                preflight_check=True,
                upload_using_accelerator=True,
            )

    mock_box_session.options.assert_called_once()


def test_update_contents_with_stream_does_preflight_check_if_specified(
        test_file,
        preflight_check,
        file_size,
        preflight_fails,
        mock_box_session,
):
    with patch.object(File, 'preflight_check', return_value=None):
        kwargs = {'file_stream': BytesIO(b'some bytes')}
        if preflight_check:
            kwargs['preflight_check'] = preflight_check
            kwargs['preflight_expected_size'] = file_size
        if preflight_fails:
            test_file.preflight_check.side_effect = BoxAPIException(400)
            with pytest.raises(BoxAPIException):
                test_file.update_contents_with_stream(**kwargs)
        else:
            test_file.update_contents_with_stream(**kwargs)

        if preflight_check:
            assert test_file.preflight_check.called_once_with(size=file_size)
            if preflight_fails:
                assert not mock_box_session.post.called
            else:
                assert mock_box_session.post.called
        else:
            assert not test_file.preflight_check.called


@patch('boxsdk.object.file.open', mock_open(read_data=b'some bytes'), create=True)
def test_update_contents_does_preflight_check_if_specified(
        test_file,
        mock_file_path,
        preflight_check,
        file_size,
        preflight_fails,
        mock_box_session,
):
    with patch.object(File, 'preflight_check', return_value=None):
        kwargs = {'file_path': mock_file_path}
        if preflight_check:
            kwargs['preflight_check'] = preflight_check
            kwargs['preflight_expected_size'] = file_size
        if preflight_fails:
            test_file.preflight_check.side_effect = BoxAPIException(400)
            with pytest.raises(BoxAPIException):
                test_file.update_contents(**kwargs)
        else:
            test_file.update_contents(**kwargs)

        if preflight_check:
            assert test_file.preflight_check.called_once_with(size=file_size)
            if preflight_fails:
                assert not mock_box_session.post.called
            else:
                assert mock_box_session.post.called
        else:
            assert not test_file.preflight_check.called


@pytest.mark.parametrize('params,expected_data', [
    ({}, {'is_download_prevented': False}),
    ({'prevent_download': False}, {'is_download_prevented': False}),
    ({'prevent_download': True}, {'is_download_prevented': True}),
    ({'expire_time': '2018-11-06T19:40:00-08:00'}, {
        'is_download_prevented': False,
        'expires_at': '2018-11-06T19:40:00-08:00'
    }),
])
def test_lock(test_file, mock_box_session, mock_file_response, params, expected_data):
    expected_url = test_file.get_url()
    expected_body = {
        'lock': {
            'type': 'lock'
        }
    }

    if 'is_download_prevented' in expected_data.keys():
        expected_body['lock']['is_download_prevented'] = expected_data['is_download_prevented']
    if 'expires_at' in expected_data.keys():
        expected_body['lock']['expires_at'] = expected_data['expires_at']

    mock_box_session.put.return_value = mock_file_response
    test_file.lock(**params)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_body),
        params=None,
        headers=None,
    )


def test_unlock(test_file, mock_box_session, mock_file_response):
    expected_url = test_file.get_url()
    mock_box_session.put.return_value = mock_file_response
    test_file.unlock()
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps({'lock': None}),
        params=None,
        headers=None,
    )


@pytest.mark.parametrize(
    'size, name, expected_data',
    [
        # Test case for specifying the name of the file for preflight
        (
            100,
            'foo.txt',
            json.dumps({'size': 100, 'name': 'foo.txt'}),
        ),

        # Test case for omitting the name of the file for preflight
        (
            200,
            None,
            json.dumps({'size': 200})
        ),
    ]
)
def test_preflight_check(
        test_file,
        mock_object_id,
        mock_box_session,
        mock_accelerator_response_for_update,
        mock_accelerator_upload_url_for_update,
        size,
        name,
        expected_data,
):
    mock_box_session.options.return_value = mock_accelerator_response_for_update
    kwargs = {'size': size}
    if name:
        kwargs['name'] = name

    accelerator_url = test_file.preflight_check(**kwargs)

    mock_box_session.options.assert_called_once_with(
        url=f'{API.BASE_API_URL}/files/{mock_object_id}/content',
        expect_json_response=True,
        data=expected_data,
    )
    assert accelerator_url == mock_accelerator_upload_url_for_update


def test_get_shared_link_download_url(
        test_file,
        mock_box_session,
        shared_link_access,
        shared_link_unshared_at,
        shared_link_password,
        shared_link_can_preview,
        shared_link_vanity_name,
        test_url,
        etag,
        if_match_header,
):
    # pylint:disable=redefined-outer-name, protected-access
    expected_url = test_file.get_url()
    mock_box_session.put.return_value.json.return_value = {
        'type': test_file.object_type,
        'id': test_file.object_id,
        'shared_link': {
            'url': None,
            'download_url': test_url,
        },
    }
    expected_data = {
        'shared_link': {},
    }
    if shared_link_access is not None:
        expected_data['shared_link']['access'] = shared_link_access
    if shared_link_unshared_at is not SDK_VALUE_NOT_SET:
        expected_data['shared_link']['unshared_at'] = shared_link_unshared_at
    if shared_link_can_preview is not None:
        expected_data['shared_link']['permissions'] = permissions = {}
        permissions['can_preview'] = shared_link_can_preview
    if shared_link_password is not None:
        expected_data['shared_link']['password'] = shared_link_password
    if shared_link_vanity_name is not None:
        expected_data['shared_link']['vanity_name'] = shared_link_vanity_name

    url = test_file.get_shared_link_download_url(
        etag=etag,
        access=shared_link_access,
        unshared_at=shared_link_unshared_at,
        password=shared_link_password,
        allow_preview=shared_link_can_preview,
        vanity_name=shared_link_vanity_name,
    )
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_data),
        headers=if_match_header,
        params=None,
    )
    assert url == test_url


def test_get_comments(test_file, mock_box_session):
    expected_url = test_file.get_url('comments')
    mock_comment1 = {
        'type': 'comment',
        'id': '11111',
        'message': 'Foo'
    }
    mock_comment2 = {
        'type': 'comment',
        'id': '22222',
        'tagged_message': 'Well hello there, @[33333:friend]!'
    }
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 2,
        'offset': 0,
        'limit': 100,
        'entries': [mock_comment1, mock_comment2]
    }
    comments = test_file.get_comments()
    comment1 = comments.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': 0})
    assert comment1.object_id == mock_comment1['id']
    assert comment1.message == mock_comment1['message']

    comment2 = comments.next()
    assert comment2.object_id == mock_comment2['id']
    assert comment2.tagged_message == mock_comment2['tagged_message']


def test_add_comment(test_file, mock_box_session, comment_params):
    expected_url = 'https://api.box.com/2.0/comments'
    comment_id = '12345'
    (message_type, message) = comment_params
    expected_data = {
        message_type: message,
        'item': {
            'type': 'file',
            'id': test_file.object_id
        }
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'comment',
        'id': comment_id,
        message_type: message
    }
    comment = test_file.add_comment(message)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert isinstance(comment, Comment)
    assert comment.object_id == comment_id


def test_get_previous_versions(test_file, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/versions'
    mock_version1 = {
        'type': 'file_version',
        'id': '11111',
        'sha1': '4788db35f85f87acaaa5ba82cc99d72c9323281f',
    }
    mock_version2 = {
        'type': 'comment',
        'id': '22222',
        'sha1': '4788db35f85f87acaaa5ba82cc99d72c9323281f',
    }
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 2,
        'offset': 0,
        'limit': 100,
        'entries': [mock_version1, mock_version2]
    }
    versions = test_file.get_previous_versions()
    version1 = versions.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': None})
    assert version1.object_id == mock_version1['id']
    assert version1.sha1 == mock_version1['sha1']

    version2 = versions.next()
    assert version2.object_id == mock_version2['id']
    assert version2.sha1 == mock_version2['sha1']


def test_promote_version(test_file, test_file_version, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/versions/current'
    sha1 = '12039d6dd9a7e6eefc78846802e'
    expected_body = {
        'type': 'file_version',
        'id': test_file_version.object_id,
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'file_version',
        'id': '77777',
        'sha1': sha1,
    }
    new_version = test_file.promote_version(test_file_version)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(new_version, FileVersion)
    assert new_version.object_id == '77777'
    assert new_version.sha1 == sha1


@pytest.mark.parametrize('params,expected_headers', [
    ({}, None),
    ({'etag': 'foobar'}, {'If-Match': 'foobar'}),
])
def test_delete_version(test_file, test_file_version, mock_box_session, params, expected_headers):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/versions/{test_file_version.object_id}'
    mock_box_session.delete.return_value.ok = True
    is_success = test_file.delete_version(test_file_version, **params)
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=expected_headers)
    assert is_success is True


def test_get_embed_url(test_file, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}'
    expected_params = {
        'fields': 'expiring_embed_link'
    }
    embed_url = 'https://app.box.com/preview/mystuff'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'file',
        'id': test_file.object_id,
        'expiring_embed_link': {
            'url': embed_url,
        },
    }

    url = test_file.get_embed_url()
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert url == embed_url


@pytest.mark.parametrize('rep_hints,expected_headers', [
    (None, None),
    ('[pdf]', {'X-Rep-Hints': '[pdf]'}),
])
def test_get_representation_info(test_file, mock_box_session, rep_hints, expected_headers):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}'
    expected_params = {'fields': 'representations'}

    info_url = 'https://api.box.com/2.0/representations/pdf'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'file',
        'id': test_file.object_id,
        'representations': {
            'total_count': 1,
            'entries': [
                {
                    'representation': 'pdf',
                    'info': {
                        'url': info_url,
                    },
                },
            ],
        },
    }

    reps = test_file.get_representation_info(rep_hints=rep_hints)
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params, headers=expected_headers)
    assert isinstance(reps, list)
    assert len(reps) == 1
    rep = reps[0]
    assert rep['representation'] == 'pdf'
    assert rep['info']['url'] == info_url


@pytest.mark.parametrize('extension,min_width,min_height,max_width,max_height,expected_params', [
    ('png', None, None, None, None, {}),
    ('png', None, None, None, None, {}),
    ('jpg', None, None, None, None, {}),
    ('png', 1, 2, None, None, {'min_width': 1, 'min_height': 2}),
    ('png', 1, 2, 3, 4, {'min_width': 1, 'min_height': 2, 'max_width': 3, 'max_height': 4}),
])
def test_get_thumbnail(
        test_file,
        mock_box_session,
        mock_content_response,
        extension,
        min_width,
        min_height,
        max_width,
        max_height,
        expected_params,
):
    expected_url = f'{API.BASE_API_URL}/files/{test_file.object_id}/thumbnail.{extension}'
    mock_box_session.get.return_value = mock_content_response

    thumb = test_file.get_thumbnail(
        extension=extension,
        min_width=min_width,
        min_height=min_height,
        max_width=max_width,
        max_height=max_height,
    )

    mock_box_session.get.assert_called_once_with(expected_url, expect_json_response=False, params=expected_params)
    assert thumb == mock_content_response.content


@pytest.mark.parametrize('dimensions,extension', [
    ('92x92', 'png'),
    ('92x92', 'jpg'),
])
def test_get_thumbnail_representation(
        test_file,
        mock_box_session,
        mock_content_response,
        dimensions,
        extension,
):
    representation_url = f'{API.BASE_API_URL}/files/{test_file.object_id}'
    content_url = 'https://dl.boxcloud.com/api/2.0/internal_files/123/versions/345/representations/jpg/content/'

    mock_representations_response = Mock()
    mock_representations_response.json.return_value = {
        'etag': '1',
        'id': test_file.object_id,
        'representations': {
            'entries': [
                {
                    'content': {
                        'url_template': content_url + '{+asset_path}'
                    },
                    'info': {
                        'url': 'https://api.box.com/2.0/internal_files/123/versions/345/representations/jpg'
                    },
                    'properties': {},
                    'representation': 'pdf',
                    'status': {
                        'state': 'success'
                    }
                }
            ]
        },
        'type': 'file'
    }

    mock_box_session.get.side_effect = [mock_representations_response, mock_content_response]

    thumb = test_file.get_thumbnail_representation(
        dimensions=dimensions,
        extension=extension,
    )

    mock_box_session.get.assert_any_call(representation_url, headers={'X-Rep-Hints': f'[{extension}?dimensions=92x92]'},
                                         params={'fields': 'representations'})
    mock_box_session.get.assert_any_call(content_url, expect_json_response=False)
    assert thumb == mock_content_response.content


def test_get_thumbnail_representation_not_found(
        test_file,
        mock_box_session,
        mock_content_response,
):
    representation_url = f'{API.BASE_API_URL}/files/{test_file.object_id}'
    dimensions = '100x100'
    extension = 'jpg'

    mock_representations_response = Mock()
    mock_representations_response.json.return_value = {
        'etag': '1',
        'id': test_file.object_id,
        'representations': {
            'entries': [],
        },
        'type': 'file'
    }

    mock_box_session.get.side_effect = [mock_representations_response, mock_content_response]

    thumb = test_file.get_thumbnail_representation(
        dimensions=dimensions,
        extension=extension,
    )

    mock_box_session.get.assert_any_call(
        representation_url,
        headers={'X-Rep-Hints': f'[{extension}?dimensions={dimensions}]'},
        params={'fields': 'representations'},
    )
    assert thumb == b''


def test_get_thumbnail_representation_not_available(
        test_file,
        mock_box_session,
        mock_content_response,
):
    representation_url = f'{API.BASE_API_URL}/files/{test_file.object_id}'
    dimensions = '100x100'
    extension = 'jpg'

    mock_representations_response = Mock()
    mock_representations_response.json.return_value = {
        'etag': '1',
        'id': test_file.object_id,
        'representations': {
            'entries': [
                {
                    'content': {
                        'url_template': 'content_url {+asset_path}'
                    },
                    'info': {
                        'url': 'https://api.box.com/2.0/internal_files/123/versions/345/representations/jpg'
                    },
                    'properties': {},
                    'representation': 'pdf',
                    'status': {'state': 'error', 'code': 'error_password_protected'}
                }
            ]
        },
        'type': 'file'
    }

    mock_box_session.get.side_effect = [mock_representations_response, mock_content_response]

    thumb = test_file.get_thumbnail_representation(
        dimensions=dimensions,
        extension=extension,
    )

    mock_box_session.get.assert_any_call(
        representation_url,
        headers={'X-Rep-Hints': f'[{extension}?dimensions={dimensions}]'},
        params={'fields': 'representations'},
    )
    assert thumb == b''
