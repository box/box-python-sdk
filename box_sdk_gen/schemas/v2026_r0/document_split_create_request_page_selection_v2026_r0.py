from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.document_split_page_selection_item_v2026_r0 import (
    DocumentSplitPageSelectionItemV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitCreateRequestPageSelectionV2026R0SplitTypeField(str, Enum):
    PAGE_SELECTION = 'page_selection'


class DocumentSplitCreateRequestPageSelectionV2026R0VersionField(str, Enum):
    V_2 = 'v_2'


class DocumentSplitCreateRequestPageSelectionV2026R0(BaseObject):
    def __init__(
        self,
        page_selection: List[DocumentSplitPageSelectionItemV2026R0],
        *,
        split_type: DocumentSplitCreateRequestPageSelectionV2026R0SplitTypeField = DocumentSplitCreateRequestPageSelectionV2026R0SplitTypeField.PAGE_SELECTION,
        version: Optional[
            DocumentSplitCreateRequestPageSelectionV2026R0VersionField
        ] = None,
        **kwargs
    ):
        """
                :param split_type: Discriminator. Must be `page_selection` for this variant., defaults to DocumentSplitCreateRequestPageSelectionV2026R0SplitTypeField.PAGE_SELECTION
                :type split_type: DocumentSplitCreateRequestPageSelectionV2026R0SplitTypeField, optional
                :param version: The version of the page selection input format. Optional. When provided
        must be `v_2`., defaults to None
                :type version: Optional[DocumentSplitCreateRequestPageSelectionV2026R0VersionField], optional
        """
        super().__init__(**kwargs)
        self.page_selection = page_selection
        self.split_type = split_type
        self.version = version
