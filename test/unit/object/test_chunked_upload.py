# coding: utf-8
# pylint: disable-msg=too-many-locals

from __future__ import unicode_literals, absolute_import
from mock import call

import io
import json
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.chunked_upload import ChunkedUpload
from boxsdk.object.upload_session import UploadSession


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
    file_size = 8
    part_bytes = b'abcdefgh'
    stream = io.BytesIO(part_bytes)
    first_sha1 = '2iNhTgJGmg18e9G9q1ycR0sZBNw='
    second_sha1 = 'A0d4GYoEXB7YC+JxzdApt2h09vw='
    third_sha1 = '+CIFFHGVe3u+u4qwiP6b1tFPQmE='
    fourth_sha1 = 'EEEXnL3aNm/XsDR/CSVfd1Fw4QM='
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
        'size': 2,
        'sha1': fourth_sha1,
    }
    parts = [part_one, part_two, part_three, part_four]
    expected_data = {
        'parts': parts,
    }
    expected_headers = {
        'Content-Type': 'application/json',
        'Digest': 'SHA=QlrxKgdDUCsyLpOgFbz4aOMk1Wo=',
    }

    expected_headers_first_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(first_sha1),
        'Content-Range': 'bytes 0-1/8',
    }
    expected_headers_second_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(second_sha1),
        'Content-Range': 'bytes 2-3/8',
    }
    expected_headers_third_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(third_sha1),
        'Content-Range': 'bytes 4-5/8',
    }
    expected_headers_fourth_upload = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(fourth_sha1),
        'Content-Range': 'bytes 6-7/8',
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
    chunked_uploader = ChunkedUpload(test_upload_session, stream, file_size)
    uploaded_file = chunked_uploader.start()
    calls = [call(expected_put_url, data=b'ab', headers=expected_headers_first_upload),
             call(expected_put_url, data=b'cd', headers=expected_headers_second_upload),
             call(expected_put_url, data=b'ef', headers=expected_headers_third_upload),
             call(expected_put_url, data=b'gh', headers=expected_headers_fourth_upload), ]
    mock_box_session.put.assert_has_calls(calls, any_order=False)
    mock_box_session.post.assert_called_once_with(expected_post_url, data=json.dumps(expected_data),
                                                  headers=expected_headers)
    assert uploaded_file.type == 'file'
    assert uploaded_file.id == '12345'
    assert uploaded_file.description == 'This is a test description'
