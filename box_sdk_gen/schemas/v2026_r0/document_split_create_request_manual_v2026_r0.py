from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.document_split_page_range_v2026_r0 import (
    DocumentSplitPageRangeV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitCreateRequestManualV2026R0SplitTypeField(str, Enum):
    MANUAL = 'manual'


class DocumentSplitCreateRequestManualV2026R0VersionField(str, Enum):
    V_1 = 'v_1'


class DocumentSplitCreateRequestManualV2026R0(BaseObject):
    def __init__(
        self,
        split_definition: List[DocumentSplitPageRangeV2026R0],
        *,
        split_type: DocumentSplitCreateRequestManualV2026R0SplitTypeField = DocumentSplitCreateRequestManualV2026R0SplitTypeField.MANUAL,
        version: Optional[DocumentSplitCreateRequestManualV2026R0VersionField] = None,
        **kwargs
    ):
        """
                :param split_definition: Page ranges that define the split. Each entry produces one output file
        containing the inclusive page range `[start, end]`.
                :type split_definition: List[DocumentSplitPageRangeV2026R0]
                :param split_type: Discriminator. Must be `manual` for this variant., defaults to DocumentSplitCreateRequestManualV2026R0SplitTypeField.MANUAL
                :type split_type: DocumentSplitCreateRequestManualV2026R0SplitTypeField, optional
                :param version: The version of the manual split input format. Omitted or `v_1` is the
        legacy `split_definition` format. Existing clients may omit this field., defaults to None
                :type version: Optional[DocumentSplitCreateRequestManualV2026R0VersionField], optional
        """
        super().__init__(**kwargs)
        self.split_definition = split_definition
        self.split_type = split_type
        self.version = version
