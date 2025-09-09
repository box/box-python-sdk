from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierBaseTypeField(str, Enum):
    SHIELD_INFORMATION_BARRIER = 'shield_information_barrier'


class ShieldInformationBarrierBase(BaseObject):
    _discriminator = 'type', {'shield_information_barrier'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierBaseTypeField] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for the shield information barrier., defaults to None
        :type id: Optional[str], optional
        :param type: The type of the shield information barrier., defaults to None
        :type type: Optional[ShieldInformationBarrierBaseTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
