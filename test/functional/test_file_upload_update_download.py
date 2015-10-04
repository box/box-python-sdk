# coding: utf-8

from __future__ import unicode_literals
from mock import mock_open, patch
import six


def test_upload_then_update(box_client, test_file_path, test_file_content, update_file_content, file_name):
    with patch('boxsdk.object.folder.open', mock_open(read_data=test_file_content), create=True):
        file_object = box_client.folder('0').upload(test_file_path, file_name)
    assert file_object.name == file_name
    file_object_with_info = file_object.get()
    assert file_object_with_info.id == file_object.object_id
    assert file_object_with_info.name == file_name
    file_content = file_object.content()
    expected_file_content = test_file_content.encode('utf-8') if isinstance(test_file_content, six.text_type)\
        else test_file_content
    assert file_content == expected_file_content
    folder_items = box_client.folder('0').get_items(100).items
    assert len(folder_items) == 1
    assert folder_items[0].object_id == file_object.object_id
    assert folder_items[0].name == file_object.name
    with patch('boxsdk.object.file.open', mock_open(read_data=update_file_content), create=True):
        updated_file_object = file_object.update_contents(test_file_path)
    assert updated_file_object.name == file_name
    file_object_with_info = updated_file_object.get()
    assert file_object_with_info.id == updated_file_object.object_id
    assert file_object_with_info.name == file_name
    file_content = updated_file_object.content()
    assert file_content == expected_file_content
    folder_items = box_client.folder('0').get_items(100).items
    assert len(folder_items) == 1
    assert folder_items[0].object_id == file_object.object_id
    assert folder_items[0].name == file_object.name


def test_upload_then_download(box_client, test_file_path, test_file_content, file_name):
    with patch('boxsdk.object.folder.open', mock_open(read_data=test_file_content), create=True):
        file_object = box_client.folder('0').upload(test_file_path, file_name)
    writeable_stream = six.BytesIO()
    file_object.download_to(writeable_stream)
    expected_file_content = test_file_content.encode('utf-8') if isinstance(test_file_content, six.text_type)\
        else test_file_content
    assert writeable_stream.getvalue() == expected_file_content
