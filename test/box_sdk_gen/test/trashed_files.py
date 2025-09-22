from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.trash_file import TrashFile

from box_sdk_gen.schemas.trash_file_restored import TrashFileRestored

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testTrashedFiles():
    file_size: int = 1024 * 1024
    file_name: str = get_uuid()
    file_byte_stream: ByteStream = generate_byte_stream(file_size)
    files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        file_byte_stream,
    )
    file: FileFull = files.entries[0]
    client.files.delete_file_by_id(file.id)
    from_trash: TrashFile = client.trashed_files.get_trashed_file_by_id(file.id)
    assert from_trash.id == file.id
    assert from_trash.name == file.name
    from_api_after_trashed: FileFull = client.files.get_file_by_id(file.id)
    assert to_string(from_api_after_trashed.item_status) == 'trashed'
    restored_file: TrashFileRestored = client.trashed_files.restore_file_from_trash(
        file.id
    )
    from_api_after_restore: FileFull = client.files.get_file_by_id(file.id)
    assert restored_file.id == from_api_after_restore.id
    assert restored_file.name == from_api_after_restore.name
    assert to_string(from_api_after_restore.item_status) == 'active'
    client.files.delete_file_by_id(file.id)
    client.trashed_files.delete_trashed_file_by_id(file.id)
    with pytest.raises(Exception):
        client.trashed_files.get_trashed_file_by_id(file.id)
