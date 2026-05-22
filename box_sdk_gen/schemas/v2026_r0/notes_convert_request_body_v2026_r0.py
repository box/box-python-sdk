from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.folder_reference_v2026_r0 import (
    FolderReferenceV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class NotesConvertRequestBodyV2026R0ContentFormatField(str, Enum):
    MARKDOWN = 'markdown'


class NotesConvertRequestBodyV2026R0(BaseObject):
    def __init__(
        self,
        content: str,
        parent: FolderReferenceV2026R0,
        name: str,
        *,
        content_format: NotesConvertRequestBodyV2026R0ContentFormatField = NotesConvertRequestBodyV2026R0ContentFormatField.MARKDOWN,
        **kwargs
    ):
        """
        :param content: The content to convert to a note. See the `content_format` field for supported formats.
        :type content: str
        :param name: The name for the created note. The `.boxnote` extension is appended automatically.
        :type name: str
        :param content_format: Format of the content to convert., defaults to NotesConvertRequestBodyV2026R0ContentFormatField.MARKDOWN
        :type content_format: NotesConvertRequestBodyV2026R0ContentFormatField, optional
        """
        super().__init__(**kwargs)
        self.content = content
        self.parent = parent
        self.name = name
        self.content_format = content_format
