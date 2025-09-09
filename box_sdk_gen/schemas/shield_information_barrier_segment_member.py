from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.shield_information_barrier_segment_member_base import (
    ShieldInformationBarrierSegmentMemberBaseTypeField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_member_base import (
    ShieldInformationBarrierSegmentMemberBase,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_member_mini import (
    ShieldInformationBarrierSegmentMemberMini,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
)

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField(
    str, Enum
):
    SHIELD_INFORMATION_BARRIER_SEGMENT = 'shield_information_barrier_segment'


class ShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentField(
    BaseObject
):
    _discriminator = 'type', {'shield_information_barrier_segment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[
            ShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField
        ] = None,
        **kwargs
    ):
        """
                :param id: The ID reference of the requesting
        shield information barrier segment., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier segment., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class ShieldInformationBarrierSegmentMember(ShieldInformationBarrierSegmentMemberMini):
    def __init__(
        self,
        *,
        shield_information_barrier: Optional[ShieldInformationBarrierBase] = None,
        shield_information_barrier_segment: Optional[
            ShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentField
        ] = None,
        created_at: Optional[DateTime] = None,
        created_by: Optional[UserBase] = None,
        updated_at: Optional[DateTime] = None,
        updated_by: Optional[UserBase] = None,
        user: Optional[UserBase] = None,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierSegmentMemberBaseTypeField] = None,
        **kwargs
    ):
        """
                :param shield_information_barrier_segment: The `type` and `id` of the requested
        shield information barrier segment., defaults to None
                :type shield_information_barrier_segment: Optional[ShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentField], optional
                :param created_at: ISO date time string when this shield
        information barrier object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param updated_at: ISO date time string when this
        shield information barrier segment Member was updated., defaults to None
                :type updated_at: Optional[DateTime], optional
                :param id: The unique identifier for the
        shield information barrier segment member., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier segment member., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentMemberBaseTypeField], optional
        """
        super().__init__(user=user, id=id, type=type, **kwargs)
        self.shield_information_barrier = shield_information_barrier
        self.shield_information_barrier_segment = shield_information_barrier_segment
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
