from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.document_split_page_selection_single_page_v2026_r0 import (
    DocumentSplitPageSelectionSinglePageV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_page_selection_page_range_v2026_r0 import (
    DocumentSplitPageSelectionPageRangeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_page_selection_segment_v2026_r0 import (
    DocumentSplitPageSelectionSegmentV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitPageSelectionItemV2026R0(BaseObject):
    def __init__(
        self,
        segments: List[DocumentSplitPageSelectionSegmentV2026R0],
        *,
        name: Optional[str] = None,
        **kwargs
    ):
        """
                :param segments: An ordered list of page segments to include in this output file. Each
        segment specifies either a single page or a contiguous page range.
                :type segments: List[DocumentSplitPageSelectionSegmentV2026R0]
                :param name: Optional name for the output file (without extension). When omitted the
        system generates a sequential name based on the source file name., defaults to None
                :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.segments = segments
        self.name = name
