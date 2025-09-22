import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.folder_locks import FolderLocks

from box_sdk_gen.schemas.folder_lock import FolderLock

from box_sdk_gen.managers.folder_locks import CreateFolderLockLockedOperations

from box_sdk_gen.managers.folder_locks import CreateFolderLockFolder

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import create_new_folder

client: BoxClient = get_default_client()


def testFolderLocks():
    folder: FolderFull = create_new_folder()
    folder_locks: FolderLocks = client.folder_locks.get_folder_locks(folder.id)
    assert len(folder_locks.entries) == 0
    folder_lock: FolderLock = client.folder_locks.create_folder_lock(
        CreateFolderLockFolder(id=folder.id, type='folder'),
        locked_operations=CreateFolderLockLockedOperations(move=True, delete=True),
    )
    assert folder_lock.folder.id == folder.id
    assert folder_lock.locked_operations.move == True
    assert folder_lock.locked_operations.delete == True
    client.folder_locks.delete_folder_lock_by_id(folder_lock.id)
    with pytest.raises(Exception):
        client.folder_locks.delete_folder_lock_by_id(folder_lock.id)
    new_folder_locks: FolderLocks = client.folder_locks.get_folder_locks(folder.id)
    assert len(new_folder_locks.entries) == 0
    client.folders.delete_folder_by_id(folder.id)
