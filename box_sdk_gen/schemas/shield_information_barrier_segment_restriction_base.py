from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierSegmentRestrictionBaseTypeField(str, Enum):
    SHIELD_INFORMATION_BARRIER_SEGMENT_RESTRICTION = (
        'shield_information_barrier_segment_restriction'
    )


class ShieldInformationBarrierSegmentRestrictionBase(BaseObject):
    _discriminator = 'type', {'shield_information_barrier_segment_restriction'}

    def __init__(
        self,
        *,
        type: Optional[ShieldInformationBarrierSegmentRestrictionBaseTypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: Shield information barrier segment restriction., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentRestrictionBaseTypeField], optional
                :param id: The unique identifier for the
        shield information barrier segment restriction., defaults to None
                :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
