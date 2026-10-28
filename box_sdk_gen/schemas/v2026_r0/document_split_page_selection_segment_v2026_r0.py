from typing import Union

from box_sdk_gen.schemas.v2026_r0.document_split_page_selection_single_page_v2026_r0 import (
    DocumentSplitPageSelectionSinglePageV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_page_selection_page_range_v2026_r0 import (
    DocumentSplitPageSelectionPageRangeV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

DocumentSplitPageSelectionSegmentV2026R0 = Union[
    DocumentSplitPageSelectionSinglePageV2026R0,
    DocumentSplitPageSelectionPageRangeV2026R0,
]
