from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiItemAskTypeField(str, Enum):
    FILE = 'file'
    HUBS = 'hubs'


class AiItemAsk(BaseObject):
    _discriminator = 'type', {'file', 'hubs'}

    def __init__(
        self,
        id: str,
        type: AiItemAskTypeField,
        *,
        content: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The ID of the file.
        :type id: str
        :param type: The type of the item. A `hubs` item must be used as a single item.
        :type type: AiItemAskTypeField
        :param content: The content of the item, often the text representation., defaults to None
        :type content: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.content = content
