from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class NotesConvertResponseV2026R0TypeField(str, Enum):
    FILE = 'file'


class NotesConvertResponseV2026R0(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        *,
        type: NotesConvertResponseV2026R0TypeField = NotesConvertResponseV2026R0TypeField.FILE,
        **kwargs
    ):
        """
        :param id: Box file ID of the created `.boxnote` file.
        :type id: str
        :param type: The Box resource type; always `file` for a Box file., defaults to NotesConvertResponseV2026R0TypeField.FILE
        :type type: NotesConvertResponseV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
