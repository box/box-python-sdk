from enum import Enum

from typing import List

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.hub_document_page_v2025_r0 import (
    HubDocumentPageV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubDocumentPagesV2025R0TypeField(str, Enum):
    DOCUMENT_PAGES = 'document_pages'


class HubDocumentPagesV2025R0(BaseObject):
    _discriminator = 'type', {'document_pages'}

    def __init__(
        self,
        entries: List[HubDocumentPageV2025R0],
        *,
        type: HubDocumentPagesV2025R0TypeField = HubDocumentPagesV2025R0TypeField.DOCUMENT_PAGES,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: Ordered list of pages.
                :type entries: List[HubDocumentPageV2025R0]
                :param type: The value will always be `document_pages`., defaults to HubDocumentPagesV2025R0TypeField.DOCUMENT_PAGES
                :type type: HubDocumentPagesV2025R0TypeField, optional
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.type = type
        self.limit = limit
        self.next_marker = next_marker
