from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListMiniV2025R0TypeField(str, Enum):
    SHIELD_LIST = 'shield_list'


class ShieldListMiniV2025R0ContentField(BaseObject):
    def __init__(self, *, type: Optional[str] = None, **kwargs):
        """
        :param type: The type of content in the shield list., defaults to None
        :type type: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type


class ShieldListMiniV2025R0(BaseObject):
    _discriminator = 'type', {'shield_list'}

    def __init__(
        self,
        id: str,
        name: str,
        content: ShieldListMiniV2025R0ContentField,
        *,
        type: ShieldListMiniV2025R0TypeField = ShieldListMiniV2025R0TypeField.SHIELD_LIST,
        **kwargs
    ):
        """
        :param id: Unique global identifier for this list.
        :type id: str
        :param name: Name of Shield List.
        :type name: str
        :param type: The type of object., defaults to ShieldListMiniV2025R0TypeField.SHIELD_LIST
        :type type: ShieldListMiniV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.content = content
        self.type = type
