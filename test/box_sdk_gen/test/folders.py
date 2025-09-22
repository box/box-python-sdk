from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.managers.folders import CopyFolderParent

from box_sdk_gen.managers.folders import UpdateFolderByIdParent

from box_sdk_gen.schemas.items import Items

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def test_get_folder_info():
    root_folder: FolderFull = client.folders.get_folder_by_id('0')
    assert root_folder.id == '0'
    assert root_folder.name == 'All Files'
    assert to_string(root_folder.type) == 'folder'


def test_get_folder_full_info_with_extra_fields():
    root_folder: FolderFull = client.folders.get_folder_by_id(
        '0', fields=['has_collaborations', 'tags']
    )
    assert root_folder.id == '0'
    assert root_folder.has_collaborations == False
    tags_length: int = len(root_folder.tags)
    assert tags_length == 0


def test_create_and_delete_folder():
    new_folder_name: str = get_uuid()
    new_folder: FolderFull = client.folders.create_folder(
        new_folder_name, CreateFolderParent(id='0')
    )
    created_folder: FolderFull = client.folders.get_folder_by_id(new_folder.id)
    assert created_folder.name == new_folder_name
    client.folders.delete_folder_by_id(new_folder.id)
    with pytest.raises(Exception):
        client.folders.get_folder_by_id(new_folder.id)


def test_update_folder():
    folder_to_update_name: str = get_uuid()
    folder_to_update: FolderFull = client.folders.create_folder(
        folder_to_update_name, CreateFolderParent(id='0')
    )
    updated_name: str = get_uuid()
    updated_folder: FolderFull = client.folders.update_folder_by_id(
        folder_to_update.id, name=updated_name, description='Updated description'
    )
    assert updated_folder.name == updated_name
    assert updated_folder.description == 'Updated description'
    client.folders.delete_folder_by_id(updated_folder.id)


def test_copy_move_folder_and_list_folder_items():
    folder_origin_name: str = get_uuid()
    folder_origin: FolderFull = client.folders.create_folder(
        folder_origin_name, CreateFolderParent(id='0')
    )
    copied_folder_name: str = get_uuid()
    copied_folder: FolderFull = client.folders.copy_folder(
        folder_origin.id, CopyFolderParent(id='0'), name=copied_folder_name
    )
    assert copied_folder.parent.id == '0'
    moved_folder_name: str = get_uuid()
    moved_folder: FolderFull = client.folders.update_folder_by_id(
        copied_folder.id,
        name=moved_folder_name,
        parent=UpdateFolderByIdParent(id=folder_origin.id),
    )
    assert moved_folder.parent.id == folder_origin.id
    folder_items: Items = client.folders.get_folder_items(folder_origin.id)
    assert folder_items.entries[0].id == moved_folder.id
    assert folder_items.entries[0].name == moved_folder_name
    client.folders.delete_folder_by_id(moved_folder.id)
    client.folders.delete_folder_by_id(folder_origin.id)
