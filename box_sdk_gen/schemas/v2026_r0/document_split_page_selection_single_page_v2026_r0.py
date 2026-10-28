from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitPageSelectionSinglePageV2026R0TypeField(str, Enum):
    SINGLE_PAGE = 'single_page'


class DocumentSplitPageSelectionSinglePageV2026R0(BaseObject):
    _discriminator = 'type', {'single_page'}

    def __init__(
        self,
        page: int,
        *,
        type: DocumentSplitPageSelectionSinglePageV2026R0TypeField = DocumentSplitPageSelectionSinglePageV2026R0TypeField.SINGLE_PAGE,
        **kwargs
    ):
        """
        :param page: A single page number to include.
        :type page: int
        :param type: Discriminator. Must be `single_page` for this variant., defaults to DocumentSplitPageSelectionSinglePageV2026R0TypeField.SINGLE_PAGE
        :type type: DocumentSplitPageSelectionSinglePageV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.page = page
        self.type = type
