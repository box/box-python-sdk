from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
)

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShieldInformationBarrierSegmentTypeField(str, Enum):
    SHIELD_INFORMATION_BARRIER_SEGMENT = 'shield_information_barrier_segment'


class ShieldInformationBarrierSegment(BaseObject):
    _discriminator = 'type', {'shield_information_barrier_segment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierSegmentTypeField] = None,
        shield_information_barrier: Optional[ShieldInformationBarrierBase] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[DateTime] = None,
        created_by: Optional[UserBase] = None,
        updated_at: Optional[DateTime] = None,
        updated_by: Optional[UserBase] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shield information barrier segment., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier segment., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentTypeField], optional
                :param name: Name of the shield information barrier segment., defaults to None
                :type name: Optional[str], optional
                :param description: Description of the shield information barrier segment., defaults to None
                :type description: Optional[str], optional
                :param created_at: ISO date time string when this shield information
        barrier object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param updated_at: ISO date time string when this
        shield information barrier segment was updated., defaults to None
                :type updated_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.shield_information_barrier = shield_information_barrier
        self.name = name
        self.description = description
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
