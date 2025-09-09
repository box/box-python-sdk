from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiItemBaseTypeField(str, Enum):
    FILE = 'file'


class AiItemBase(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        *,
        type: AiItemBaseTypeField = AiItemBaseTypeField.FILE,
        content: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The ID of the file.
        :type id: str
        :param type: The type of the item. Currently the value can be `file` only., defaults to AiItemBaseTypeField.FILE
        :type type: AiItemBaseTypeField, optional
        :param content: The content of the item, often the text representation., defaults to None
        :type content: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.content = content
