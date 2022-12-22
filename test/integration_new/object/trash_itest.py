from datetime import datetime

import pytest
from boxsdk.pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from boxsdk.pagination.marker_based_object_collection import MarkerBasedObjectCollection

from test.integration_new import util
from test.integration_new import CLIENT
from test.integration_new.context_managers.box_test_file import BoxTestFile
from test.integration_new.context_managers.box_test_folder import BoxTestFolder

FILE_TESTS_DIRECTORY_NAME = 'file-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=f'{FILE_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder:
        yield folder


def test_trash_get_items(parent_folder, small_file_path):
    name = f'{util.random_name()}.pdf'
    test_file = parent_folder.upload(file_path=small_file_path, file_name=name)
    test_file.delete()
    trash_items = CLIENT.trash().get_items()
    for item in trash_items:
        if item.id == test_file.object_id:
            assert item.type == test_file.object_type
            assert item.name == test_file.name
            CLIENT.trash().permanently_delete_item(item)
            break


def test_trash_restore_item(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        test_file.delete()
        trash_items = CLIENT.trash().get_items()
        for item in trash_items:
            if item.id == test_file.object_id:
                assert item.type == test_file.object_type
                assert item.name == test_file.name
                CLIENT.trash().restore_item(item)
                break
        folder_items = parent_folder.get_items()
        for item in folder_items:
            if item.id == test_file.object_id:
                assert item.type == test_file.object_type
                assert item.name == test_file.name
                break


def test_trash_get_items_with_offset(parent_folder, small_file_path):
    name = f'{util.random_name()}.pdf'
    test_file = parent_folder.upload(file_path=small_file_path, file_name=name)
    test_file.delete()
    trash_items = CLIENT.trash().get_items(limit=1, offset=1)
    assert isinstance(trash_items, LimitOffsetBasedObjectCollection)
    for item in trash_items:
        if item.id == test_file.object_id:
            assert item.type == test_file.object_type
            assert item.name == test_file.name
            CLIENT.trash().permanently_delete_item(item)
            break


def test_trash_get_items_with_marker(parent_folder, small_file_path, other_client):
    name = f'{util.random_name()}.pdf'
    test_file = parent_folder.upload(file_path=small_file_path, file_name=name)
    test_file.delete()
    trash_items = other_client.trash().get_items(limit=1, use_marker=True)
    assert isinstance(trash_items, MarkerBasedObjectCollection)
    for item in trash_items:
        if item.id == test_file.object_id:
            assert item.type == test_file.object_type
            assert item.name == test_file.name
            other_client.trash().permanently_delete_item(item)
            break
