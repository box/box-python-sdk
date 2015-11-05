# coding: utf-8

from __future__ import unicode_literals
from mock import patch
import pytest
from boxsdk.client import Client
from boxsdk.exception import BoxAPIException
from test.util.streamable_mock_open import streamable_mock_open


def test_upload_then_delete(box_client, test_file_path, test_file_content, file_name):
    with patch('boxsdk.object.folder.open', streamable_mock_open(read_data=test_file_content), create=True):
        file_object = box_client.folder('0').upload(test_file_path, file_name)
    assert file_object.delete()
    assert len(box_client.folder('0').get_items(1)) == 0


def test_create_folder_then_update_info(box_client, folder_name):
    folder = box_client.folder('0').create_subfolder(folder_name)
    assert folder.delete()
    assert len(box_client.folder('0').get_items(1)) == 0


@pytest.mark.parametrize('constructor', [Client.file, Client.folder])
def test_get_item_info_for_missing_file(box_client, constructor):
    with pytest.raises(BoxAPIException) as exc_info:
        constructor(box_client, '1').delete()
    assert exc_info.value.status == 404
