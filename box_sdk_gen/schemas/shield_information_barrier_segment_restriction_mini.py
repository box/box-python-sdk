from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction_base import (
    ShieldInformationBarrierSegmentRestrictionBaseTypeField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction_base import (
    ShieldInformationBarrierSegmentRestrictionBase,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentTypeField(
    str, Enum
):
    SHIELD_INFORMATION_BARRIER_SEGMENT = 'shield_information_barrier_segment'


class ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentField(
    BaseObject
):
    _discriminator = 'type', {'shield_information_barrier_segment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[
            ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentTypeField
        ] = None,
        **kwargs
    ):
        """
                :param id: The ID reference of the
        requesting shield information barrier segment., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier segment., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentTypeField(
    str, Enum
):
    SHIELD_INFORMATION_BARRIER_SEGMENT = 'shield_information_barrier_segment'


class ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentField(BaseObject):
    _discriminator = 'type', {'shield_information_barrier_segment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[
            ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentTypeField
        ] = None,
        **kwargs
    ):
        """
                :param id: The ID reference of the
        restricted shield information barrier segment., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information segment., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class ShieldInformationBarrierSegmentRestrictionMini(
    ShieldInformationBarrierSegmentRestrictionBase
):
    def __init__(
        self,
        shield_information_barrier_segment: ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentField,
        restricted_segment: ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentField,
        *,
        type: Optional[ShieldInformationBarrierSegmentRestrictionBaseTypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
                :param shield_information_barrier_segment: The `type` and `id` of the
        requested shield information barrier segment.
                :type shield_information_barrier_segment: ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentField
                :param restricted_segment: The `type` and `id` of the
        restricted shield information barrier segment.
                :type restricted_segment: ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentField
                :param type: Shield information barrier segment restriction., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentRestrictionBaseTypeField], optional
                :param id: The unique identifier for the
        shield information barrier segment restriction., defaults to None
                :type id: Optional[str], optional
        """
        super().__init__(type=type, id=id, **kwargs)
        self.shield_information_barrier_segment = shield_information_barrier_segment
        self.restricted_segment = restricted_segment
