import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.watermark import Watermark

from box_sdk_gen.managers.file_watermarks import UpdateFileWatermarkWatermark

from box_sdk_gen.managers.file_watermarks import (
    UpdateFileWatermarkWatermarkImprintField,
)

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testCreateGetDeleteFileWatermark():
    file_name: str = ''.join([get_uuid(), '.txt'])
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(10),
    )
    file: FileFull = uploaded_files.entries[0]
    created_watermark: Watermark = client.file_watermarks.update_file_watermark(
        file.id,
        UpdateFileWatermarkWatermark(
            imprint=UpdateFileWatermarkWatermarkImprintField.DEFAULT
        ),
    )
    watermark: Watermark = client.file_watermarks.get_file_watermark(file.id)
    client.file_watermarks.delete_file_watermark(file.id)
    with pytest.raises(Exception):
        client.file_watermarks.get_file_watermark(file.id)
    client.files.delete_file_by_id(file.id)
