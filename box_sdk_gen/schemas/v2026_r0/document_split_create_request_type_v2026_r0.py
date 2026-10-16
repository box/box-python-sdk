from typing import Union

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_manual_v2026_r0 import (
    DocumentSplitCreateRequestManualV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_page_selection_v2026_r0 import (
    DocumentSplitCreateRequestPageSelectionV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_smart_v2026_r0 import (
    DocumentSplitCreateRequestSmartV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

DocumentSplitCreateRequestTypeV2026R0 = Union[
    DocumentSplitCreateRequestManualV2026R0,
    DocumentSplitCreateRequestPageSelectionV2026R0,
    DocumentSplitCreateRequestSmartV2026R0,
]
