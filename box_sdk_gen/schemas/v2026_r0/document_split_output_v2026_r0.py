from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.file_reference_v2026_r0 import FileReferenceV2026R0

from box_sdk_gen.schemas.v2026_r0.document_split_page_range_v2026_r0 import (
    DocumentSplitPageRangeV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitOutputV2026R0(BaseObject):
    def __init__(
        self,
        *,
        generated_files: Optional[List[FileReferenceV2026R0]] = None,
        split_definition: Optional[List[DocumentSplitPageRangeV2026R0]] = None,
        **kwargs
    ):
        """
                :param generated_files: References to the files that were created by the split., defaults to None
                :type generated_files: Optional[List[FileReferenceV2026R0]], optional
                :param split_definition: The page ranges that Box produced for a `smart` split. Each entry
        corresponds to one generated file with the inclusive page range
        `[start, end]`. Omitted or `null` for `manual` splits, where the
        caller-supplied ranges are available in `split_input.split_definition`.
        Omitted for `page_selection` splits, where the caller-supplied page
        layout is available in `split_input.page_selection`., defaults to None
                :type split_definition: Optional[List[DocumentSplitPageRangeV2026R0]], optional
        """
        super().__init__(**kwargs)
        self.generated_files = generated_files
        self.split_definition = split_definition
