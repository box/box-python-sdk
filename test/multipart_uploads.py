from io import BytesIO, RawIOBase

from box_sdk_gen.client import BoxClient
from box_sdk_gen.internal.utils import (
    generate_byte_buffer,
    get_uuid,
    read_byte_stream,
)
from box_sdk_gen.managers.uploads import (
    UploadFileAttributes,
    UploadFileAttributesParentField,
    UploadFileVersionAttributes,
)
from box_sdk_gen.schemas.file_full import FileFull

from test.commons import get_default_client

client: BoxClient = get_default_client()


class NonSeekableStream(RawIOBase):
    def __init__(self, content: bytes):
        self._content = BytesIO(content)

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return False

    def readinto(self, buffer) -> int:
        chunk = self._content.read(len(buffer))
        buffer[: len(chunk)] = chunk
        return len(chunk)


def testUploadFileAndFileVersionFromNonSeekableStream():
    content: bytes = generate_byte_buffer(5 * 1024 * 1024)
    new_file_name: str = get_uuid()
    uploaded_file: FileFull = client.uploads.upload_file(
        UploadFileAttributes(
            name=new_file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        NonSeekableStream(content),
    ).entries[0]
    try:
        assert uploaded_file.name == new_file_name
        assert uploaded_file.size == len(content)
        assert read_byte_stream(client.downloads.download_file(uploaded_file.id)) == (
            content
        )

        new_content: bytes = generate_byte_buffer(1024 * 1024)
        new_file_version: FileFull = client.uploads.upload_file_version(
            uploaded_file.id,
            UploadFileVersionAttributes(name=get_uuid()),
            NonSeekableStream(new_content),
        ).entries[0]
        assert new_file_version.size == len(new_content)
        assert read_byte_stream(client.downloads.download_file(uploaded_file.id)) == (
            new_content
        )
    finally:
        client.files.delete_file_by_id(uploaded_file.id)
