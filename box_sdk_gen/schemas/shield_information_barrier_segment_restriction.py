from typing import Optional

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction_base import (
    ShieldInformationBarrierSegmentRestrictionBaseTypeField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction_base import (
    ShieldInformationBarrierSegmentRestrictionBase,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction_mini import (
    ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction_mini import (
    ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction_mini import (
    ShieldInformationBarrierSegmentRestrictionMini,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
)

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShieldInformationBarrierSegmentRestriction(
    ShieldInformationBarrierSegmentRestrictionMini
):
    def __init__(
        self,
        shield_information_barrier_segment: ShieldInformationBarrierSegmentRestrictionMiniShieldInformationBarrierSegmentField,
        restricted_segment: ShieldInformationBarrierSegmentRestrictionMiniRestrictedSegmentField,
        *,
        shield_information_barrier: Optional[ShieldInformationBarrierBase] = None,
        created_at: Optional[DateTime] = None,
        created_by: Optional[UserBase] = None,
        updated_at: Optional[DateTime] = None,
        updated_by: Optional[UserBase] = None,
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
                :param created_at: ISO date time string when this
        shield information barrier
        Segment Restriction object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param updated_at: ISO date time string when this
        shield information barrier segment
        Restriction was updated., defaults to None
                :type updated_at: Optional[DateTime], optional
                :param type: Shield information barrier segment restriction., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentRestrictionBaseTypeField], optional
                :param id: The unique identifier for the
        shield information barrier segment restriction., defaults to None
                :type id: Optional[str], optional
        """
        super().__init__(
            shield_information_barrier_segment=shield_information_barrier_segment,
            restricted_segment=restricted_segment,
            type=type,
            id=id,
            **kwargs
        )
        self.shield_information_barrier = shield_information_barrier
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
