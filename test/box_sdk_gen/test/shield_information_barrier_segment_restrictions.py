import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.shield_information_barrier import ShieldInformationBarrier

from box_sdk_gen.schemas.shield_information_barrier_segment import (
    ShieldInformationBarrierSegment,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBaseTypeField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction import (
    ShieldInformationBarrierSegmentRestriction,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionType,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegment,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentTypeField,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionRestrictedSegment,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentTypeField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_restrictions import (
    ShieldInformationBarrierSegmentRestrictions,
)

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from test.box_sdk_gen.test.commons import get_or_create_shield_information_barrier


def testShieldInformationBarrierSegmentRestrictions():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    barrier: ShieldInformationBarrier = get_or_create_shield_information_barrier(
        client, enterprise_id
    )
    barrier_id: str = barrier.id
    segment: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.create_shield_information_barrier_segment(
            ShieldInformationBarrierBase(
                id=barrier_id,
                type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER,
            ),
            get_uuid(),
            description='barrier segment description',
        )
    )
    segment_id: str = segment.id
    segment_to_restrict: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.create_shield_information_barrier_segment(
            ShieldInformationBarrierBase(
                id=barrier_id,
                type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER,
            ),
            get_uuid(),
            description='barrier segment description',
        )
    )
    segment_to_restrict_id: str = segment_to_restrict.id
    segment_restriction: ShieldInformationBarrierSegmentRestriction = (
        client.shield_information_barrier_segment_restrictions.create_shield_information_barrier_segment_restriction(
            CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegment(
                id=segment_id,
                type=CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT,
            ),
            CreateShieldInformationBarrierSegmentRestrictionRestrictedSegment(
                id=segment_to_restrict_id,
                type=CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT,
            ),
            type=CreateShieldInformationBarrierSegmentRestrictionType.SHIELD_INFORMATION_BARRIER_SEGMENT_RESTRICTION,
        )
    )
    segment_restriction_id: str = segment_restriction.id
    assert segment_restriction.shield_information_barrier_segment.id == segment_id
    segment_restrictions: ShieldInformationBarrierSegmentRestrictions = (
        client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restrictions(
            segment_id
        )
    )
    assert len(segment_restrictions.entries) > 0
    segment_restriction_from_api: ShieldInformationBarrierSegmentRestriction = (
        client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restriction_by_id(
            segment_restriction_id
        )
    )
    assert segment_restriction_from_api.id == segment_restriction_id
    assert (
        segment_restriction_from_api.shield_information_barrier_segment.id == segment_id
    )
    assert segment_restriction_from_api.restricted_segment.id == segment_to_restrict_id
    assert segment_restriction_from_api.shield_information_barrier.id == barrier_id
    client.shield_information_barrier_segment_restrictions.delete_shield_information_barrier_segment_restriction_by_id(
        segment_restriction_id
    )
    with pytest.raises(Exception):
        client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restriction_by_id(
            segment_restriction_id
        )
    client.shield_information_barrier_segments.delete_shield_information_barrier_segment_by_id(
        segment_id
    )
    client.shield_information_barrier_segments.delete_shield_information_barrier_segment_by_id(
        segment_to_restrict_id
    )
