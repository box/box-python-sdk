# coding: utf-8

from __future__ import unicode_literals, absolute_import

import base64
import hashlib
from io import BytesIO
import json
import pytest

from boxsdk.config import API
from boxsdk.object.file import File
from boxsdk.object.upload_session import UploadSession


@pytest.fixture()
def test_upload_session(mock_box_session):
    upload_session_response_object = {
        'part_size': 8,
        'total_parts': 10,
    }
    return UploadSession(mock_box_session, '11493C07ED3EABB6E59874D3A1EF3581', upload_session_response_object)


def test_get_parts(test_upload_session, mock_box_session):
    expected_url = '{0}/files/upload_sessions/{1}/parts'.format(API.UPLOAD_URL, test_upload_session.object_id)

    parts = mock_box_session.get.return_value.json.return_value = {
        'entries': [
            {
                'part': {
                    'part_id': '8F0966B1',
                    'offset': 0,
                    'size': 8,
                    'sha1': None,
                },
            },
        ],
    }
    test_parts = test_upload_session.get_parts()
    mock_box_session.get.assert_called_once_with(expected_url)
    assert test_parts == parts['entries']


def test_abort(test_upload_session, mock_box_session):
    expected_url = '{0}/files/upload_sessions/{1}'.format(API.UPLOAD_URL, test_upload_session.object_id)
    mock_box_session.delete.return_value.ok = True
    result = test_upload_session.abort()
    mock_box_session.delete.assert_called_once_with(expected_url)
    assert result is True


def test_upload_part(test_upload_session, mock_box_session):
    expected_url = '{0}/files/upload_sessions/{1}'.format(API.UPLOAD_URL, test_upload_session.object_id)
    chunk = BytesIO(b'abcdefgh')
    offset = 32
    total_size = 80
    expected_sha1 = 'QlrxKgdDUCsyLpOgFbz4aOMk1Wo='
    expected_headers = {
        'Content-Type': 'application/octet-stream',
        'Digest': 'SHA={}'.format(expected_sha1),
        'Content-Range': 'bytes 32-39/80',
    }
    mock_box_session.put.return_value.json.return_value = {
        'part': {
            'part_id': 'ABCDEF123',
            'offset': offset,
            'size': 8,
            'sha1': expected_sha1,
        },
    }
    part = test_upload_session.upload_part(chunk, offset, total_size)

    mock_box_session.put.assert_called_once_with(expected_url, data=chunk, headers=expected_headers)
    assert part['part']['sha1'] == expected_sha1


def test_commit(test_upload_session, mock_box_session):
    expected_url = '{0}/files/upload_sessions/{1}/commit'.format(API.UPLOAD_URL, test_upload_session.object_id)
    sha1 = hashlib.sha1()
    sha1.update(b'fake_file_data')
    file_id = '12345'
    parts = [
        {
            'part_id': 'ABCDEF123',
            'offset': 0,
            'size': 8,
            'sha1': 'fake_sha1',
        },
        {
            'part_id': 'ABCDEF456',
            'offset': 8,
            'size': 8,
            'sha1': 'fake_sha1',
        },
    ]
    expected_data = {
        'parts': parts,
    }
    expected_headers = {
        'Content-Type': 'application/json',
        'Digest': 'SHA={}'.format(base64.b64encode(sha1.digest()).decode('utf-8')),
    }

    mock_box_session.post.return_value.json.return_value = {
        'entries': [
            {
                'type': 'file',
                'id': file_id,
            },
        ],
    }
    created_file = test_upload_session.commit(parts, sha1.digest())
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=expected_headers)
    assert isinstance(created_file, File)
    assert created_file.id == file_id
