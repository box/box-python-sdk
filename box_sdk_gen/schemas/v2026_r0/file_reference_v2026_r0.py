from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class FileReferenceV2026R0TypeField(str, Enum):
    FILE = 'file'


class FileReferenceV2026R0(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        *,
        type: FileReferenceV2026R0TypeField = FileReferenceV2026R0TypeField.FILE,
        **kwargs
    ):
        """
        :param id: ID of the file.
        :type id: str
        :param type: The value will always be `file`., defaults to FileReferenceV2026R0TypeField.FILE
        :type type: FileReferenceV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
