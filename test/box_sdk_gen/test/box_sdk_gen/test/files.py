from typing import Optional

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.managers.files import GetFileThumbnailUrlExtension

from box_sdk_gen.internal.utils import Buffer

from box_sdk_gen.managers.files import GetFileThumbnailByIdExtension

from box_sdk_gen.schemas.trash_file import TrashFile

from box_sdk_gen.managers.files import UpdateFileByIdLock

from box_sdk_gen.managers.files import UpdateFileByIdLockAccessField

from box_sdk_gen.managers.files import CopyFileParent

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import read_byte_stream

from box_sdk_gen.internal.utils import generate_byte_stream_from_buffer

from box_sdk_gen.internal.utils import generate_byte_buffer

from box_sdk_gen.internal.utils import buffer_equals

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.internal.utils import create_null

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def upload_file(file_name: str, file_stream: ByteStream) -> FileFull:
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        file_stream,
    )
    return uploaded_files.entries[0]


def testGetFileThumbnailUrl():
    thumbnail_file_name: str = get_uuid()
    thumbnail_content_stream: ByteStream = generate_byte_stream(1024 * 1024)
    thumbnail_file: FileFull = upload_file(
        thumbnail_file_name, thumbnail_content_stream
    )
    download_url: str = client.files.get_file_thumbnail_url(
        thumbnail_file.id, GetFileThumbnailUrlExtension.PNG
    )
    assert not download_url == None
    assert 'https://' in download_url
    client.files.delete_file_by_id(thumbnail_file.id)


def testGetFileThumbnail():
    thumbnail_file_name: str = get_uuid()
    thumbnail_buffer: Buffer = generate_byte_buffer(1024 * 1024)
    thumbnail_content_stream: ByteStream = generate_byte_stream_from_buffer(
        thumbnail_buffer
    )
    thumbnail_file: FileFull = upload_file(
        thumbnail_file_name, thumbnail_content_stream
    )
    thumbnail: Optional[ByteStream] = client.files.get_file_thumbnail_by_id(
        thumbnail_file.id, GetFileThumbnailByIdExtension.PNG
    )
    assert not buffer_equals(read_byte_stream(thumbnail), thumbnail_buffer) == True
    client.files.delete_file_by_id(thumbnail_file.id)


def testGetFileFullExtraFields():
    new_file_name: str = get_uuid()
    file_stream: ByteStream = generate_byte_stream(1024 * 1024)
    uploaded_file: FileFull = upload_file(new_file_name, file_stream)
    file: FileFull = client.files.get_file_by_id(
        uploaded_file.id, fields=['is_externally_owned', 'has_collaborations']
    )
    assert file.is_externally_owned == False
    assert file.has_collaborations == False
    client.files.delete_file_by_id(file.id)


def testCreateGetAndDeleteFile():
    new_file_name: str = get_uuid()
    updated_content_stream: ByteStream = generate_byte_stream(1024 * 1024)
    uploaded_file: FileFull = upload_file(new_file_name, updated_content_stream)
    file: FileFull = client.files.get_file_by_id(uploaded_file.id)
    with pytest.raises(Exception):
        client.files.get_file_by_id(
            uploaded_file.id,
            fields=['name'],
            extra_headers={'if-none-match': file.etag},
        )
    assert file.name == new_file_name
    client.files.delete_file_by_id(uploaded_file.id)
    trashed_file: TrashFile = client.trashed_files.get_trashed_file_by_id(
        uploaded_file.id
    )
    assert file.id == trashed_file.id


def testUpdateFile():
    file_to_update: FileFull = upload_new_file()
    updated_name: str = get_uuid()
    updated_file: FileFull = client.files.update_file_by_id(
        file_to_update.id, name=updated_name, description='Updated description'
    )
    assert updated_file.name == updated_name
    assert updated_file.description == 'Updated description'
    client.files.delete_file_by_id(updated_file.id)


def testFileLock():
    file: FileFull = upload_new_file()
    file_with_lock: FileFull = client.files.update_file_by_id(
        file.id,
        lock=UpdateFileByIdLock(access=UpdateFileByIdLockAccessField.LOCK),
        fields=['lock'],
    )
    assert not file_with_lock.lock == None
    file_without_lock: FileFull = client.files.update_file_by_id(
        file.id, lock=create_null(), fields=['lock']
    )
    assert file_without_lock.lock == None
    client.files.delete_file_by_id(file.id)


def testCopyFile():
    file_origin: FileFull = upload_new_file()
    copied_file_name: str = get_uuid()
    copied_file: FileFull = client.files.copy_file(
        file_origin.id, CopyFileParent(id='0'), name=copied_file_name
    )
    assert copied_file.parent.id == '0'
    assert copied_file.name == copied_file_name
    client.files.delete_file_by_id(file_origin.id)
    client.files.delete_file_by_id(copied_file.id)
