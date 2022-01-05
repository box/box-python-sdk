# coding: utf-8

import base64
import hashlib
import io
import json
import pytest

from mock import patch
from boxsdk.config import API
from boxsdk.util.chunked_uploader import ChunkedUploader
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
    expected_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}/parts'
    mock_entry = {
        'part_id': '8F0966B1',
        'offset': 0,
        'size': 8,
        'sha1': None,
    }
    mock_box_session.get.return_value.json.return_value = {
        'entries': [mock_entry],
        'offset': 0,
        'total_count': 1,
        'limit': 1000,
    }
    test_parts = test_upload_session.get_parts()
    part = test_parts.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': None})
    assert isinstance(part, dict)
    assert part['part_id'] == mock_entry['part_id']
    assert part['size'] == mock_entry['size']
    assert part['offset'] == mock_entry['offset']


def test_abort(test_upload_session, mock_box_session):
    expected_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}'
    mock_box_session.delete.return_value.ok = True
    result = test_upload_session.abort()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
    assert result is True


def test_upload_part_bytes(test_upload_session, mock_box_session):
    expected_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}'
    part_bytes = b'abcdefgh'
    offset = 32
    total_size = 80
    expected_sha1 = 'QlrxKgdDUCsyLpOgFbz4aOMk1Wo='
    expected_headers = {
        'Content-Type': 'application/octet-stream',
        'Digest': f'SHA={expected_sha1}',
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
    part = test_upload_session.upload_part_bytes(part_bytes, offset, total_size)

    mock_box_session.put.assert_called_once_with(expected_url, data=part_bytes, headers=expected_headers)
    assert isinstance(part, dict)
    assert part['sha1'] == expected_sha1
    assert part['size'] == 8
    assert part['part_id'] == 'ABCDEF123'


def test_commit(test_upload_session, mock_box_session):
    expected_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}/commit'
    sha1 = hashlib.sha1()
    sha1.update(b'fake_file_data')
    file_id = '12345'
    file_type = 'file'
    file_etag = '7'
    file_attributes = {'description': 'This is a test description.'}
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
        'attributes': file_attributes,
        'parts': parts,
    }
    expected_headers = {
        'Content-Type': 'application/json',
        'Digest': f'SHA={base64.b64encode(sha1.digest()).decode("utf-8")}',
        'If-Match': '7',
    }
    mock_box_session.post.return_value.json.return_value = {
        'entries': [
            {
                'type': file_type,
                'id': file_id,
                'description': 'This is a test description.',
            },
        ],
    }
    created_file = test_upload_session.commit(content_sha1=sha1.digest(), parts=parts, file_attributes=file_attributes, etag=file_etag)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=expected_headers)
    assert isinstance(created_file, File)
    assert created_file.id == file_id
    assert created_file.type == file_type
    assert created_file.description == 'This is a test description.'


def test_commit_with_missing_params(test_upload_session, mock_box_session):
    expected_get_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}/parts'
    expected_url = f'{API.UPLOAD_URL}/files/upload_sessions/{test_upload_session.object_id}/commit'
    sha1 = hashlib.sha1()
    sha1.update(b'fake_file_data')
    file_id = '12345'
    file_type = 'file'
    parts = [
        {
            'part_id': '8F0966B1',
            'offset': 0,
            'size': 8,
            'sha1': None,
        },
    ]
    expected_data = {
        'parts': parts,
    }
    expected_headers = {
        'Content-Type': 'application/json',
        'Digest': f'SHA={base64.b64encode(sha1.digest()).decode("utf-8")}',
    }
    mock_entry = {
        'part_id': '8F0966B1',
        'offset': 0,
        'size': 8,
        'sha1': None,
    }
    mock_box_session.get.return_value.json.return_value = {
        'entries': [mock_entry],
        'offset': 0,
        'total_count': 1,
        'limit': 1000,
    }
    mock_box_session.post.return_value.json.return_value = {
        'entries': [
            {
                'type': file_type,
                'id': file_id,
            },
        ],
    }
    created_file = test_upload_session.commit(content_sha1=sha1.digest())
    mock_box_session.get.assert_called_once_with(expected_get_url, params={'offset': None})
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=expected_headers)
    assert isinstance(created_file, File)
    assert created_file.id == file_id
    assert created_file.type == file_type


def test_get_chunked_uploader_for_stream(test_upload_session):
    file_size = 197520
    part_bytes = b'abcdefgh'
    stream = io.BytesIO(part_bytes)
    chunked_uploader = test_upload_session.get_chunked_uploader_for_stream(stream, file_size)
    assert isinstance(chunked_uploader, ChunkedUploader)


def test_get_chunked_uploader(mock_content_response, mock_file_path, test_upload_session):
    mock_file_stream = io.BytesIO(mock_content_response.content)
    file_size = 197520
    with patch('os.stat') as stat:
        stat.return_value.st_size = file_size
        with patch('boxsdk.object.upload_session.open', return_value=mock_file_stream):
            chunked_uploader = test_upload_session.get_chunked_uploader(mock_file_path)
    assert isinstance(chunked_uploader, ChunkedUploader)
