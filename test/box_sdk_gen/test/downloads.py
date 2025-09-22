from typing import Optional

from box_sdk_gen.client import BoxClient

from box_sdk_gen.internal.utils import Buffer

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.internal.utils import OutputStream

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_buffer

from box_sdk_gen.internal.utils import generate_byte_stream_from_buffer

from box_sdk_gen.internal.utils import buffer_equals

from box_sdk_gen.internal.utils import read_byte_stream

from box_sdk_gen.internal.utils import get_file_output_stream

from box_sdk_gen.internal.utils import close_file_output_stream

from box_sdk_gen.internal.utils import read_buffer_from_file

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

client: BoxClient = get_default_client()


def test_download_file():
    new_file_name: str = get_uuid()
    file_buffer: Buffer = generate_byte_buffer(1024 * 1024)
    file_content_stream: ByteStream = generate_byte_stream_from_buffer(file_buffer)
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=new_file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        file_content_stream,
    )
    uploaded_file: FileFull = uploaded_files.entries[0]
    downloaded_file_content: Optional[ByteStream] = client.downloads.download_file(
        uploaded_file.id
    )
    assert buffer_equals(read_byte_stream(downloaded_file_content), file_buffer)
    client.files.delete_file_by_id(uploaded_file.id)


def test_get_download_url():
    uploaded_file: FileFull = upload_new_file()
    download_url: str = client.downloads.get_download_file_url(uploaded_file.id)
    assert not download_url == None
    assert 'https://' in download_url
    client.files.delete_file_by_id(uploaded_file.id)


def test_download_file_to_output_stream():
    new_file_name: str = get_uuid()
    file_buffer: Buffer = generate_byte_buffer(1024 * 1024)
    file_content_stream: ByteStream = generate_byte_stream_from_buffer(file_buffer)
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=new_file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        file_content_stream,
    )
    uploaded_file: FileFull = uploaded_files.entries[0]
    file_output_stream: OutputStream = get_file_output_stream(new_file_name)
    client.downloads.download_file_to_output_stream(
        uploaded_file.id, file_output_stream
    )
    close_file_output_stream(file_output_stream)
    downloaded_file_content: Buffer = read_buffer_from_file(new_file_name)
    assert buffer_equals(downloaded_file_content, file_buffer)
    client.files.delete_file_by_id(uploaded_file.id)
