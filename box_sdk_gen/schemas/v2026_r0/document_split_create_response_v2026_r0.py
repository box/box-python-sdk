from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitCreateResponseV2026R0TypeField(str, Enum):
    DOCUMENT_SPLIT = 'document_split'


class DocumentSplitCreateResponseV2026R0(BaseObject):
    _discriminator = 'type', {'document_split'}

    def __init__(
        self,
        id: str,
        *,
        type: DocumentSplitCreateResponseV2026R0TypeField = DocumentSplitCreateResponseV2026R0TypeField.DOCUMENT_SPLIT,
        **kwargs
    ):
        """
        :param id: The unique identifier of the created Document Split job.
        :type id: str
        :param type: The value will always be `document_split`., defaults to DocumentSplitCreateResponseV2026R0TypeField.DOCUMENT_SPLIT
        :type type: DocumentSplitCreateResponseV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
