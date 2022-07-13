import json
from datetime import datetime
import pytest
import pytz

from boxsdk.config import API
from boxsdk.object.folder import Folder
from boxsdk.object.file_request import FileRequest
from boxsdk.object.file_request import StatusState


def test_get(test_file_request, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/file_requests/{test_file_request.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': test_file_request.object_type,
        'id': test_file_request.object_id,
        'title': 'File Request'
    }
    file_request = test_file_request.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(file_request, FileRequest)
    assert file_request['type'] == file_request.object_type
    assert file_request['id'] == file_request.object_id
    assert file_request['title'] == 'File Request'


def test_update(test_file_request, mock_box_session):
    new_title = 'New File Request Title'
    new_status = StatusState.INACTIVE
    expected_url = f'{API.BASE_API_URL}/file_requests/{test_file_request.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': test_file_request.object_type,
        'id': test_file_request.object_id,
        'title': new_title,
        'status': new_status,
    }
    data = {
        'title': new_title,
        'status': StatusState.INACTIVE,
    }
    file_request = test_file_request.update_info(data=data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(file_request, FileRequest)
    assert file_request['type'] == test_file_request.object_type
    assert file_request['id'] == test_file_request.object_id
    assert file_request['title'] == new_title
    assert file_request['status'] == StatusState.INACTIVE


@pytest.mark.parametrize('expires_at', [
    '2019-07-01T22:02:24+14:00',
    datetime(2019, 7, 1, 22, 2, 24, tzinfo=pytz.timezone('US/Alaska'))
])
def test_copy(test_file_request, mock_box_session, expires_at):
    new_folder_id = '100'
    expected_url = f'{API.BASE_API_URL}/file_requests/{test_file_request.object_id}/copy'
    expected_expires_at = '2019-07-01T22:02:24+14:00'
    mock_box_session.post.return_value.json.return_value = {
        'type': test_file_request.object_type,
        'id': test_file_request.object_id,
        'title': 'File Request Copied',
        'folder': {
            'type': 'folder',
            'id': new_folder_id,
        },
        'expires_at': expected_expires_at,
    }
    new_title = 'File Request Copied'
    new_folder = Folder(mock_box_session, object_id=new_folder_id)
    file_request = test_file_request.copy(title=new_title, folder=new_folder, expires_at=expires_at)
    data = {
        'folder': {
            'id': new_folder_id,
            'type': 'folder',
        },
        'title': new_title,
        'expires_at': expected_expires_at,
    }
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(data))
    assert isinstance(file_request, FileRequest)
    assert file_request['type'] == test_file_request.object_type
    assert file_request['title'] == 'File Request Copied'
    assert file_request['folder']['id'] == '100'
    assert file_request['folder']['type'] == 'folder'


def test_delete(test_file_request, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/file_requests/{test_file_request.object_id}'
    test_file_request.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
