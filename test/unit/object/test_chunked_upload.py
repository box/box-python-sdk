# coding: utf-8
# pylint: disable-msg=too-many-locals

from __future__ import unicode_literals, absolute_import

import io
import json
import pytest

from mock import Mock, call
from boxsdk.config import API
from boxsdk.exception import BoxException
from boxsdk.object.file import File
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


def test_start(test_upload_session, mock_box_session):
    expected_put_url = '{0}/files/upload_sessions/{1}'.format(API.UPLOAD_URL, test_upload_session.object_id)
    expected_post_url = '{0}/files/upload_sessions/{1}/commit'.format(API.UPLOAD_URL, test_upload_session.object_id)
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
        'Digest': 'SHA={}'.format(first_sha1),
        'Content-Range': 'bytes 0-1/7',
    }
    expected_headers_second_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(second_sha1),
        'Content-Range': 'bytes 2-3/7',
    }
    expected_headers_third_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(third_sha1),
        'Content-Range': 'bytes 4-5/7',
    }
    expected_headers_fourth_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(fourth_sha1),
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
    mock_box_session.put.side_effect = [first_response_mock, second_response_mock,
                                        third_response_mock, fourth_response_mock]
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
    calls = [call(expected_put_url, data=b'ab', headers=expected_headers_first_upload),
             call(expected_put_url, data=b'cd', headers=expected_headers_second_upload),
             call(expected_put_url, data=b'ef', headers=expected_headers_third_upload),
             call(expected_put_url, data=b'g', headers=expected_headers_fourth_upload), ]
    flaky_stream.read.assert_has_calls([call(2), call(2), call(2), call(1), call(2), call(2), call(1)], any_order=False)
    mock_box_session.put.assert_has_calls(calls, any_order=False)
    mock_box_session.post.assert_called_once_with(expected_post_url, data=json.dumps(expected_data),
                                                  headers=expected_headers)
    assert uploaded_file.type == 'file'
    assert uploaded_file.id == '12345'
    assert uploaded_file.description == 'This is a test description'
    assert isinstance(uploaded_file, File)
    assert uploaded_file._session == mock_box_session  # pylint:disable=protected-access


def test_abort():
    file_size = 7
    part_bytes = b'abcdefg'
    stream = io.BytesIO(part_bytes)
    upload_session_mock_object = Mock(UploadSession)
    chunked_uploader = ChunkedUploader(upload_session_mock_object, stream, file_size)
    upload_session_mock_object.abort.return_value = True
    is_aborted = chunked_uploader.abort()
    try:
        chunked_uploader.start()
    except BoxException:
        pass
    assert upload_session_mock_object.abort.called
    assert is_aborted is True
