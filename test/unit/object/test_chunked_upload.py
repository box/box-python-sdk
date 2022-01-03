# coding: utf-8
# pylint: disable-msg=too-many-locals

import io
import json
import pytest

from mock import MagicMock, Mock, call
from boxsdk.config import API
from boxsdk.exception import BoxAPIException
from boxsdk.exception import BoxException
from boxsdk.object.file import File
from boxsdk.pagination.limit_offset_based_dict_collection import LimitOffsetBasedDictCollection
from boxsdk.object.upload_session import UploadSession
from boxsdk.util.chunked_uploader import ChunkedUploader


@pytest.fixture()
def test_upload_session(mock_box_session):
    upload_session_response_object = {
        'total_parts': 4,
        'part_size': 2,
        'session_expires_at': '2017-11-09T21:59:16Z',
        'id': 'D5E3F7ADA11A38A0A66AD0B64AACA658',
        'type': 'upload_session',
        'num_parts_processed': 0
    }
    return UploadSession(mock_box_session, 'D5E3F7ADA11A38A0A66AD0B64AACA658', upload_session_response_object)


@pytest.fixture()
def mock_upload_session():
    upload_session_mock_object = Mock(UploadSession)
    upload_session_mock_object.total_parts = 4
    upload_session_mock_object.part_size = 2
    upload_session_mock_object.id = 'F971964745A5CD0C001BZ4E58196BFD'
    upload_session_mock_object.type = 'upload_session'
    upload_session_mock_object.num_parts_processed = 0
    return upload_session_mock_object


def test_start(test_upload_session, mock_box_session):
    expected_put_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}'
    expected_post_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}/commit'
    file_size = 7
    first_sha1 = '2iNhTgJGmg18e9G9q1ycR0sZBNw='
    second_sha1 = 'A0d4GYoEXB7YC+JxzdApt2h09vw='
    third_sha1 = '+CIFFHGVe3u+u4qwiP6b1tFPQmE='
    fourth_sha1 = 'VP0XESCfscB4EJI3QTLGbnniJBs='
    part_one = {
        'part_id': 'CFEB4BA9',
        'offset': 0,
        'size': 2,
        'sha1': first_sha1,
    }
    part_two = {
        'part_id': '4DBB872D',
        'offset': 2,
        'size': 2,
        'sha1': second_sha1,
    }
    part_three = {
        'part_id': '6F2D3486',
        'offset': 4,
        'size': 2,
        'sha1': third_sha1,
    }
    part_four = {
        'part_id': '4DBC872D',
        'offset': 6,
        'size': 1,
        'sha1': fourth_sha1,
    }
    parts = [part_one, part_two, part_three, part_four]
    expected_data = {
        'parts': parts,
    }
    expected_headers = {
        'Content-Type': 'application/json',
        'Digest': 'SHA=L7XhNBn8iSRoZeejJPR27GJOh0A=',
    }

    expected_headers_first_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': f'SHA={first_sha1}',
        'Content-Range': 'bytes 0-1/7',
    }
    expected_headers_second_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': f'SHA={second_sha1}',
        'Content-Range': 'bytes 2-3/7',
    }
    expected_headers_third_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': f'SHA={third_sha1}',
        'Content-Range': 'bytes 4-5/7',
    }
    expected_headers_fourth_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': f'SHA={fourth_sha1}',
        'Content-Range': 'bytes 6-6/7',
    }

    first_response_mock = Mock()
    second_response_mock = Mock()
    third_response_mock = Mock()
    fourth_response_mock = Mock()

    first_response_mock.json.return_value = {
        'part': part_one
    }
    second_response_mock.json.return_value = {
        'part': part_two
    }
    third_response_mock.json.return_value = {
        'part': part_three
    }
    fourth_response_mock.json.return_value = {
        'part': part_four
    }
    mock_box_session.put.side_effect = [
        first_response_mock,
        second_response_mock,
        third_response_mock,
        fourth_response_mock
    ]
    mock_box_session.post.return_value.json.return_value = {
        'entries': [
            {
                'type': 'file',
                'id': '12345',
                'description': 'This is a test description',
            }
        ]
    }
    flaky_stream = Mock()
    flaky_stream.read.side_effect = [b'ab', None, b'c', b'd', b'ef', b'g', b'']

    chunked_uploader = ChunkedUploader(test_upload_session, flaky_stream, file_size)
    uploaded_file = chunked_uploader.start()
    calls = [
        call(expected_put_url, data=b'ab', headers=expected_headers_first_upload),
        call(expected_put_url, data=b'cd', headers=expected_headers_second_upload),
        call(expected_put_url, data=b'ef', headers=expected_headers_third_upload),
        call(expected_put_url, data=b'g', headers=expected_headers_fourth_upload),
    ]
    flaky_stream.read.assert_has_calls([call(2), call(2), call(2), call(1), call(2), call(2), call(1)], any_order=False)
    mock_box_session.put.assert_has_calls(calls, any_order=False)
    mock_box_session.post.assert_called_once_with(
        expected_post_url,
        data=json.dumps(expected_data),
        headers=expected_headers
    )
    assert uploaded_file.type == 'file'
    assert uploaded_file.id == '12345'
    assert uploaded_file.description == 'This is a test description'
    assert isinstance(uploaded_file, File)
    assert uploaded_file._session == mock_box_session  # pylint:disable=protected-access


def test_resume_cross_process(test_file, mock_upload_session):
    file_size = 7
    part_bytes = b'abcdefg'
    stream = io.BytesIO(part_bytes)
    part_one = {
        'part_id': 'CFEB4BA9',
        'offset': 0,
        'size': 2,
        'sha1': None,
    }
    part_two = {
        'part_id': '4DBB872D',
        'offset': 2,
        'size': 2,
        'sha1': None,
    }
    part_three = {
        'part_id': '6F2D3486',
        'offset': 4,
        'size': 2,
        'sha1': None,
    }
    part_four = {
        'part_id': '4DBC872D',
        'offset': 6,
        'size': 1,
        'sha1': None,
    }
    parts = [part_one, part_two, part_three, part_four]
    mock_upload_session.commit.return_value = test_file
    mock_iterator = MagicMock(LimitOffsetBasedDictCollection)
    mock_iterator.__iter__.return_value = [part_one, part_four]
    mock_upload_session.get_parts.return_value = mock_iterator
    mock_upload_session.upload_part_bytes.side_effect = [part_two, part_three]
    chunked_uploader = ChunkedUploader(mock_upload_session, stream, file_size)
    uploaded_file = chunked_uploader.resume()
    calls = [
        call(offset=2, part_bytes=b'cd', total_size=7),
        call(offset=4, part_bytes=b'ef', total_size=7),
    ]
    mock_upload_session.upload_part_bytes.assert_has_calls(calls, any_order=False)
    mock_upload_session.commit.assert_called_once_with(
        content_sha1=b'/\xb5\xe14\x19\xfc\x89$he\xe7\xa3$\xf4v\xecbN\x87@',
        parts=parts
    )
    assert uploaded_file is test_file


def test_resume_in_process(test_file, mock_upload_session):
    file_size = 7
    part_bytes = b'abcdefg'
    stream = io.BytesIO(part_bytes)
    first_part = {
        'part_id': 'CFEB4BA9',
        'offset': 0,
        'size': 2,
        'sha1': '2iNhTgJGmg18e9G9q1ycR0sZBNw=',
    }
    second_part = {
        'part_id': '4DBB872D',
        'offset': 2,
        'size': 2,
        'sha1': 'A0d4GYoEXB7YC+JxzdApt2h09vw=',
    }
    third_part = {
        'part_id': '6F2D3486',
        'offset': 4,
        'size': 2,
        'sha1': '+CIFFHGVe3u+u4qwiP6b1tFPQmE=',
    }
    fourth_part = {
        'part_id': '4DBC872D',
        'offset': 6,
        'size': 1,
        'sha1': 'VP0XESCfscB4EJI3QTLGbnniJBs=',
    }
    parts = [first_part, second_part, third_part, fourth_part]
    mock_iterator = MagicMock(LimitOffsetBasedDictCollection)
    mock_iterator.__iter__.return_value = [first_part, second_part, third_part]
    mock_upload_session.get_parts.return_value = mock_iterator
    mock_upload_session.upload_part_bytes.side_effect = [third_part]
    mock_upload_session.commit.return_value = test_file
    chunked_uploader = ChunkedUploader(mock_upload_session, stream, file_size)
    mock_upload_session.upload_part_bytes.side_effect = [
        first_part,
        second_part,
        BoxAPIException(502),
        fourth_part
    ]
    try:
        chunked_uploader.start()
    except BoxAPIException:
        uploaded_file = chunked_uploader.resume()
    calls = [call(offset=6, part_bytes=b'g', total_size=7)]
    mock_upload_session.upload_part_bytes.assert_has_calls(calls, any_order=False)
    mock_upload_session.commit.assert_called_once_with(
        content_sha1=b'/\xb5\xe14\x19\xfc\x89$he\xe7\xa3$\xf4v\xecbN\x87@',
        parts=parts
    )
    assert uploaded_file is test_file


def test_abort_with_start(mock_upload_session):
    file_size = 7
    part_bytes = b'abcdefg'
    stream = io.BytesIO(part_bytes)
    chunked_uploader = ChunkedUploader(mock_upload_session, stream, file_size)
    mock_upload_session.abort.return_value = True
    is_aborted = chunked_uploader.abort()
    try:
        chunked_uploader.start()
    except BoxException:
        pass
    mock_upload_session.abort.assert_called_once_with()
    assert is_aborted is True


def test_abort_with_resume(mock_upload_session):
    file_size = 7
    part_bytes = b'abcdefg'
    stream = io.BytesIO(part_bytes)
    chunked_uploader = ChunkedUploader(mock_upload_session, stream, file_size)
    mock_upload_session.abort.return_value = True
    is_aborted = chunked_uploader.abort()
    try:
        chunked_uploader.resume()
    except BoxException:
        pass
    mock_upload_session.abort.assert_called_once_with()
    assert is_aborted is True
