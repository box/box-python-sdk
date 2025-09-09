from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class FileVersionBaseV2025R0TypeField(str, Enum):
    FILE_VERSION = 'file_version'


class FileVersionBaseV2025R0(BaseObject):
    _discriminator = 'type', {'file_version'}

    def __init__(
        self,
        id: str,
        *,
        type: FileVersionBaseV2025R0TypeField = FileVersionBaseV2025R0TypeField.FILE_VERSION,
        **kwargs
    ):
        """
        :param id: The unique identifier that represent a file version.
        :type id: str
        :param type: The value will always be `file_version`., defaults to FileVersionBaseV2025R0TypeField.FILE_VERSION
        :type type: FileVersionBaseV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
