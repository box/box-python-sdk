
import json
import pytest

from boxsdk.config import API
from boxsdk.object.trash import Trash


@pytest.fixture()
def test_trash(mock_box_session):
    return Trash(mock_box_session)


@pytest.fixture(params=('file', 'folder', 'web_link'))
def test_item_and_response(
        test_file,
        mock_file_response,
        test_folder,
        mock_folder_response,
        test_web_link,
        mock_web_link_response,
        request,
):
    if request.param == 'file':
        return test_file, mock_file_response
    if request.param == 'web_link':
        return test_web_link, mock_web_link_response
    return test_folder, mock_folder_response


def test_get_from_trash(test_item_and_response, test_trash, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = f'{API.BASE_API_URL}/{test_item.object_type + "s"}/{test_item.object_id}/trash'
    mock_box_session.get.return_value.json.return_value = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'created_at': '2015-05-07T14:31:16-07:00',
        'modified_at': '2015-05-07T14:31:16-07:00',
        'created_by': {
            'type': 'user',
            'id': '11111',
        },
    }
    trashed_item_info = test_trash.get_item(item=test_item, fields=['created_at', 'modified_at'])
    mock_box_session.get.assert_called_once_with(expected_url, params={'fields': 'created_at,modified_at'})
    assert isinstance(trashed_item_info, test_item.__class__)
    assert trashed_item_info.object_type == test_item.object_type
    assert trashed_item_info.object_id == test_item.object_id
    assert trashed_item_info.created_at == '2015-05-07T14:31:16-07:00'
    assert trashed_item_info.modified_at == '2015-05-07T14:31:16-07:00'
    assert trashed_item_info.created_by['type'] == 'user'
    assert trashed_item_info.created_by['id'] == '11111'


def test_restore_from_trash(test_item_and_response, test_trash, test_folder, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    new_name = 'New Name'
    expected_url = f'{API.BASE_API_URL}/{test_item.object_type + "s"}/{test_item.object_id}'
    value = json.dumps({
        'name': new_name,
        'parent': {
            'id': test_folder.object_id,
        },
    })
    mock_box_session.post.return_value.json.return_value = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'created_at': '2015-05-07T14:31:16-07:00',
        'modified_at': '2015-05-07T14:31:16-07:00',
        'created_by': {
            'type': 'user',
            'id': '11111',
        },
    }
    restored_item = test_trash.restore_item(test_item, new_name, test_folder, ['created_at', 'modified_at'])
    mock_box_session.post.assert_called_once_with(expected_url, data=value, params={'fields': 'created_at,modified_at'})
    assert isinstance(restored_item, test_item.__class__)
    assert restored_item.object_type == test_item.object_type
    assert restored_item.object_id == test_item.object_id
    assert restored_item.created_at == '2015-05-07T14:31:16-07:00'
    assert restored_item.modified_at == '2015-05-07T14:31:16-07:00'
    assert restored_item.created_by['type'] == 'user'
    assert restored_item.created_by['id'] == '11111'


def test_permanently_delete(test_item_and_response, test_trash, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = f'{API.BASE_API_URL}/{test_item.object_type + "s"}/{test_item.object_id}/trash'
    mock_box_session.delete.return_value.ok = True
    info = test_trash.permanently_delete_item(test_item)
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False)
    assert info is True


def test_get_trashed_items(test_item_and_response, test_trash, mock_box_session):
    test_item, _ = test_item_and_response
    item_name = 'Test Trashed Item'
    expected_url = f'{API.BASE_API_URL}/folders/trash/items'
    mock_trash = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'name': 'Test Trashed Item'
    }
    mock_box_session.get.return_value.json.return_value = {
        'total_count': 5,
        'offset': 0,
        'limit': 100,
        'entries': [mock_trash]
    }
    trashed_items = test_trash.get_items(fields=['name'])
    trashed_item = trashed_items.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'fields': 'name', 'offset': None})
    assert isinstance(trashed_item, test_item.__class__)
    assert trashed_item.type == mock_trash['type']
    assert trashed_item.id == mock_trash['id']
    assert trashed_item.name == item_name
