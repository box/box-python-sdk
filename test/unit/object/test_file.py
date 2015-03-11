# coding: utf-8

from __future__ import unicode_literals
import json
from mock import mock_open, patch
import pytest
from six import BytesIO
from boxsdk.config import API

from boxsdk.object.file import File


# pylint:disable=protected-access


def test_delete_file(test_file, mock_box_session, etag, if_match_header):
    test_file.delete(etag=etag)
    expected_url = test_file.get_url()
    mock_box_session.delete.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params={},
        headers=if_match_header,
    )


def test_download_to(test_file, mock_box_session, mock_content_response):
    expected_url = test_file.get_url('content')
    mock_box_session.get.return_value = mock_content_response
    mock_writeable_stream = BytesIO()
    test_file.download_to(mock_writeable_stream)
    mock_writeable_stream.seek(0)
    assert mock_writeable_stream.read() == mock_content_response.content
    mock_box_session.get.assert_called_once_with(expected_url, expect_json_response=False, stream=True)


def test_get_content(test_file, mock_box_session, mock_content_response):
    expected_url = test_file.get_url('content')
    mock_box_session.get.return_value = mock_content_response
    file_content = test_file.content()
    assert file_content == mock_content_response.content
    mock_box_session.get.assert_called_once_with(expected_url, expect_json_response=False)


@pytest.mark.parametrize('is_stream', (True, False))
def test_update_content(
        test_file,
        mock_box_session,
        mock_content_response,
        mock_upload_response,
        mock_file_path,
        etag,
        if_match_header,
        is_stream,
):
    expected_url = test_file.get_url('content').replace(API.BASE_API_URL, API.UPLOAD_URL)
    mock_box_session.post.return_value = mock_upload_response

    if is_stream:
        mock_file_stream = BytesIO(mock_content_response.content)
        new_file = test_file.update_contents_with_stream(mock_file_stream, etag=etag)
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        mock_file_stream = mock_file.return_value
        with patch('boxsdk.object.file.open', mock_file, create=True):
            new_file = test_file.update_contents(mock_file_path, etag=etag)

    mock_files = {'file': ('unused', mock_file_stream)}
    mock_box_session.post.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        files=mock_files,
        headers=if_match_header,
    )
    assert isinstance(new_file, File)
    assert new_file.object_id == mock_upload_response.json()['entries'][0]['id']


@pytest.mark.parametrize('prevent_download', (True, False))
def test_lock(test_file, mock_box_session, mock_file_response, prevent_download):
    expected_url = test_file.get_url()
    mock_box_session.put.return_value = mock_file_response
    test_file.lock(prevent_download)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps({'lock': {'is_download_prevented': prevent_download, 'type': 'lock'}}),
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
