from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubItemV2025R0TypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'
    WEB_LINK = 'web_link'


class HubItemV2025R0(BaseObject):
    _discriminator = 'type', {'file', 'folder', 'web_link'}

    def __init__(self, id: str, type: HubItemV2025R0TypeField, name: str, **kwargs):
        """
        :param id: The unique identifier for this item.
        :type id: str
        :param type: The type of the item.
        :type type: HubItemV2025R0TypeField
        :param name: The name of the item.
        :type name: str
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
