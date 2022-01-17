# coding: utf-8
from test.util.streamable_mock_open import streamable_mock_open

from io import BytesIO
from mock import patch


def test_upload_then_update(box_client, test_file_path, test_file_content, update_file_content, file_name):
    with patch('boxsdk.object.folder.open', streamable_mock_open(read_data=test_file_content), create=True):
        file_object = box_client.folder('0').upload(test_file_path, file_name)
    assert file_object.name == file_name
    file_object_with_info = file_object.get()
    assert file_object_with_info.id == file_object.object_id
    assert file_object_with_info.name == file_name
    file_content = file_object.content()
    expected_file_content = test_file_content.encode('utf-8') if isinstance(test_file_content, str)\
        else test_file_content
    assert file_content == expected_file_content
    folder_items = box_client.folder('0').get_items(100)
    item = folder_items.next()
    item_count = 1
    for _ in folder_items:
        item_count += 1
    assert item_count == 1
    assert item.object_id == file_object.object_id
    assert item.name == file_object.name
    with patch('boxsdk.object.file.open', streamable_mock_open(read_data=update_file_content), create=True):
        updated_file_object = file_object.update_contents(test_file_path)
    assert updated_file_object.name == file_name
    file_object_with_info = updated_file_object.get()
    assert file_object_with_info.id == updated_file_object.object_id
    assert file_object_with_info.name == file_name
    file_content = updated_file_object.content()
    expected_file_content = update_file_content.encode('utf-8') if isinstance(update_file_content, str)\
        else update_file_content
    assert file_content == expected_file_content
    folder_items = box_client.folder('0').get_items(100)
    item = folder_items.next()
    item_count = 1
    for _ in folder_items:
        item_count += 1
    assert item_count == 1
    assert item.object_id == file_object.object_id
    assert item.name == file_object.name


def test_upload_then_download(box_client, test_file_path, test_file_content, file_name):
    with patch('boxsdk.object.folder.open', streamable_mock_open(read_data=test_file_content), create=True):
        file_object = box_client.folder('0').upload(test_file_path, file_name)
    writeable_stream = BytesIO()
    file_object.download_to(writeable_stream)
    expected_file_content = test_file_content.encode('utf-8') if isinstance(test_file_content, str)\
        else test_file_content
    assert writeable_stream.getvalue() == expected_file_content
