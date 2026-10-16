from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitPageSelectionPageRangeV2026R0TypeField(str, Enum):
    PAGE_RANGE = 'page_range'


class DocumentSplitPageSelectionPageRangeV2026R0(BaseObject):
    _discriminator = 'type', {'page_range'}

    def __init__(
        self,
        start: int,
        end: int,
        *,
        type: DocumentSplitPageSelectionPageRangeV2026R0TypeField = DocumentSplitPageSelectionPageRangeV2026R0TypeField.PAGE_RANGE,
        **kwargs
    ):
        """
        :param start: The first page (inclusive) included in this segment.
        :type start: int
        :param end: The last page (inclusive) included in this segment.
        :type end: int
        :param type: Discriminator. Must be `page_range` for this variant., defaults to DocumentSplitPageSelectionPageRangeV2026R0TypeField.PAGE_RANGE
        :type type: DocumentSplitPageSelectionPageRangeV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.type = type
