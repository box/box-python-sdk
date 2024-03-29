from logging import Logger
from io import BytesIO
from unittest.mock import patch, Mock
from test.util.streamable_mock_open import streamable_mock_open
import pytest

from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.network import default_network


@pytest.fixture
def logger():
    return Mock(Logger)


@pytest.fixture(autouse=True)
def mocked_logger(logger):
    with patch.object(default_network, 'getLogger') as get_logger:
        get_logger.return_value = logger
        yield


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


def test_do_not_log_downloaded_file_content_stream(box_client, test_file_path, test_file_content, file_name, logger):
    with patch('boxsdk.object.folder.open', streamable_mock_open(read_data=test_file_content), create=True):
        file_object = box_client.folder('0').upload(test_file_path, file_name)
    writeable_stream = BytesIO()

    file_object.download_to(writeable_stream)

    expected_file_content = test_file_content.encode('utf-8') if isinstance(test_file_content, str) \
        else test_file_content
    assert writeable_stream.getvalue() == expected_file_content
    assert logger.info.call_args[0][1]['content'] == DefaultNetworkResponse.CONTENT_NOT_LOGGED


def test_do_not_log_content_of_downloaded_file(box_client, test_file_path, test_file_content, file_name, logger):
    with patch('boxsdk.object.folder.open', streamable_mock_open(read_data=test_file_content), create=True):
        file_object = box_client.folder('0').upload(test_file_path, file_name)

    file_content = file_object.content()

    expected_file_content = test_file_content.encode('utf-8') if isinstance(test_file_content, str) \
        else test_file_content
    assert file_content == expected_file_content
    assert logger.info.call_args[0][1]['content'] == DefaultNetworkResponse.CONTENT_NOT_LOGGED
