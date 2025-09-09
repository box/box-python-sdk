from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class FileReferenceV2025R0TypeField(str, Enum):
    FILE = 'file'


class FileReferenceV2025R0(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        *,
        type: FileReferenceV2025R0TypeField = FileReferenceV2025R0TypeField.FILE,
        **kwargs
    ):
        """
        :param id: ID of the object.
        :type id: str
        :param type: The value will always be `file`., defaults to FileReferenceV2025R0TypeField.FILE
        :type type: FileReferenceV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
