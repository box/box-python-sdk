from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitCreateRequestSmartV2026R0SplitTypeField(str, Enum):
    SMART = 'smart'


class DocumentSplitCreateRequestSmartV2026R0(BaseObject):
    def __init__(
        self,
        prompt: str,
        *,
        split_type: DocumentSplitCreateRequestSmartV2026R0SplitTypeField = DocumentSplitCreateRequestSmartV2026R0SplitTypeField.SMART,
        **kwargs
    ):
        """
        :param prompt: A natural language prompt that guides automatic page range detection.
        :type prompt: str
        :param split_type: Discriminator. Must be `smart` for this variant., defaults to DocumentSplitCreateRequestSmartV2026R0SplitTypeField.SMART
        :type split_type: DocumentSplitCreateRequestSmartV2026R0SplitTypeField, optional
        """
        super().__init__(**kwargs)
        self.prompt = prompt
        self.split_type = split_type
