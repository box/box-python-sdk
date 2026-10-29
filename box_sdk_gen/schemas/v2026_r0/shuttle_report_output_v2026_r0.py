from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleReportOutputV2026R0TypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class ShuttleReportOutputV2026R0(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(self, id: str, type: ShuttleReportOutputV2026R0TypeField, **kwargs):
        """
        :param id: The unique identifier of the generated Box file or folder.
        :type id: str
        :param type: The Box object type of the generated file or folder.
        :type type: ShuttleReportOutputV2026R0TypeField
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
