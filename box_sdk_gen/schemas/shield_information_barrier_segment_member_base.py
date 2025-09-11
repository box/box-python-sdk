from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierSegmentMemberBaseTypeField(str, Enum):
    SHIELD_INFORMATION_BARRIER_SEGMENT_MEMBER = (
        'shield_information_barrier_segment_member'
    )


class ShieldInformationBarrierSegmentMemberBase(BaseObject):
    _discriminator = 'type', {'shield_information_barrier_segment_member'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierSegmentMemberBaseTypeField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the
        shield information barrier segment member., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier segment member., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentMemberBaseTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
