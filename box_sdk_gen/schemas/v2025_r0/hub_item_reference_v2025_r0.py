from typing import Union

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.folder_reference_v2025_r0 import (
    FolderReferenceV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.weblink_reference_v2025_r0 import (
    WeblinkReferenceV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError

HubItemReferenceV2025R0 = Union[
    FileReferenceV2025R0, FolderReferenceV2025R0, WeblinkReferenceV2025R0
]
