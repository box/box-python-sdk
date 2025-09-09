from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiCitationTypeField(str, Enum):
    FILE = 'file'


class AiCitation(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        *,
        content: Optional[str] = None,
        id: Optional[str] = None,
        type: Optional[AiCitationTypeField] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param content: The specific content from where the answer was referenced., defaults to None
        :type content: Optional[str], optional
        :param id: The id of the item., defaults to None
        :type id: Optional[str], optional
        :param type: The type of the item., defaults to None
        :type type: Optional[AiCitationTypeField], optional
        :param name: The name of the item., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.content = content
        self.id = id
        self.type = type
        self.name = name
