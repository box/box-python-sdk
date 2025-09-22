import pytest

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.managers.uploads import UploadFileVersionAttributes

from box_sdk_gen.managers.uploads import UploadWithPreflightCheckAttributes

from box_sdk_gen.managers.uploads import UploadWithPreflightCheckAttributesParentField

from box_sdk_gen.schemas.upload_url import UploadUrl

from box_sdk_gen.managers.uploads import PreflightFileUploadCheckParent

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.client import BoxClient

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testUploadFileAndFileVersion():
    new_file_name: str = get_uuid()
    file_content_stream: ByteStream = generate_byte_stream(1024 * 1024)
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=new_file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        file_content_stream,
    )
    uploaded_file: FileFull = uploaded_files.entries[0]
    assert uploaded_file.name == new_file_name
    new_file_version_name: str = get_uuid()
    new_file_content_stream: ByteStream = generate_byte_stream(1024 * 1024)
    uploaded_files_version: Files = client.uploads.upload_file_version(
        uploaded_file.id,
        UploadFileVersionAttributes(name=new_file_version_name),
        new_file_content_stream,
    )
    new_file_version: FileFull = uploaded_files_version.entries[0]
    assert new_file_version.name == new_file_version_name
    client.files.delete_file_by_id(new_file_version.id)


def testUploadFileWithPreflightCheck():
    new_file_name: str = get_uuid()
    file_content_stream: ByteStream = generate_byte_stream(1024 * 1024)
    with pytest.raises(Exception):
        client.uploads.upload_with_preflight_check(
            UploadWithPreflightCheckAttributes(
                name=new_file_name,
                size=-1,
                parent=UploadWithPreflightCheckAttributesParentField(id='0'),
            ),
            file_content_stream,
        )
    upload_files_with_preflight: Files = client.uploads.upload_with_preflight_check(
        UploadWithPreflightCheckAttributes(
            name=new_file_name,
            size=1024 * 1024,
            parent=UploadWithPreflightCheckAttributesParentField(id='0'),
        ),
        file_content_stream,
    )
    file: FileFull = upload_files_with_preflight.entries[0]
    assert file.name == new_file_name
    assert file.size == 1024 * 1024
    with pytest.raises(Exception):
        client.uploads.upload_with_preflight_check(
            UploadWithPreflightCheckAttributes(
                name=new_file_name,
                size=1024 * 1024,
                parent=UploadWithPreflightCheckAttributesParentField(id='0'),
            ),
            file_content_stream,
        )
    client.files.delete_file_by_id(file.id)


def testPreflightCheck():
    new_file_name: str = get_uuid()
    preflight_check_result: UploadUrl = client.uploads.preflight_file_upload_check(
        name=new_file_name,
        size=1024 * 1024,
        parent=PreflightFileUploadCheckParent(id='0'),
    )
    assert not preflight_check_result.upload_url == ''
