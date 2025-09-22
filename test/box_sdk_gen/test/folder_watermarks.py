import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.schemas.watermark import Watermark

from box_sdk_gen.managers.folder_watermarks import UpdateFolderWatermarkWatermark

from box_sdk_gen.managers.folder_watermarks import (
    UpdateFolderWatermarkWatermarkImprintField,
)

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testCreateGetDeleteFolderWatermark():
    folder_name: str = get_uuid()
    folder: FolderFull = client.folders.create_folder(
        folder_name, CreateFolderParent(id='0')
    )
    created_watermark: Watermark = client.folder_watermarks.update_folder_watermark(
        folder.id,
        UpdateFolderWatermarkWatermark(
            imprint=UpdateFolderWatermarkWatermarkImprintField.DEFAULT
        ),
    )
    watermark: Watermark = client.folder_watermarks.get_folder_watermark(folder.id)
    client.folder_watermarks.delete_folder_watermark(folder.id)
    with pytest.raises(Exception):
        client.folder_watermarks.get_folder_watermark(folder.id)
    client.folders.delete_folder_by_id(folder.id)
