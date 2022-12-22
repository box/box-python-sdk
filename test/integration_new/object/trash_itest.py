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
    try:
        trash_items = CLIENT.trash().get_items()
        assert test_file.id in [item.id for item in trash_items]
    finally:
        CLIENT.trash().permanently_delete_item(test_file)


def test_trash_restore_item(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        test_file.delete()
        trash_items = CLIENT.trash().get_items()
        assert test_file.id in [item.id for item in trash_items]
        CLIENT.trash().restore_item(test_file)
        folder_items = parent_folder.get_items()
        assert test_file.id in [item.id for item in folder_items]


def test_trash_get_items_with_offset(parent_folder, small_file_path):
    name = f'{util.random_name()}.pdf'
    test_file = parent_folder.upload(file_path=small_file_path, file_name=name)
    test_file.delete()
    try:
        trash_items = CLIENT.trash().get_items()
        assert isinstance(trash_items, LimitOffsetBasedObjectCollection)
        assert test_file.id in [item.id for item in trash_items]
    finally:
        CLIENT.trash().permanently_delete_item(test_file)


def test_trash_get_items_with_marker(parent_folder, small_file_path):
    name = f'{util.random_name()}.pdf'
    test_file = parent_folder.upload(file_path=small_file_path, file_name=name)
    test_file.delete()
    try:
        trash_items = CLIENT.trash().get_items(limit=100, use_marker=True)
        assert isinstance(trash_items, MarkerBasedObjectCollection)
        assert test_file.id in [item.id for item in trash_items]
    finally:
        CLIENT.trash().permanently_delete_item(test_file)
