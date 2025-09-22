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

from box_sdk_gen.schemas.shield_information_barrier_segment_member import (
    ShieldInformationBarrierSegmentMember,
)

from box_sdk_gen.managers.shield_information_barrier_segment_members import (
    CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegment,
)

from box_sdk_gen.managers.shield_information_barrier_segment_members import (
    CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField,
)

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.schemas.shield_information_barrier_segment_members import (
    ShieldInformationBarrierSegmentMembers,
)

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from test.box_sdk_gen.test.commons import get_or_create_shield_information_barrier


def testShieldInformationBarrierSegmentMembers():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    barrier: ShieldInformationBarrier = get_or_create_shield_information_barrier(
        client, enterprise_id
    )
    barrier_id: str = barrier.id
    segment_name: str = get_uuid()
    segment: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.create_shield_information_barrier_segment(
            ShieldInformationBarrierBase(
                id=barrier_id,
                type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER,
            ),
            segment_name,
        )
    )
    assert segment.name == segment_name
    segment_member: ShieldInformationBarrierSegmentMember = (
        client.shield_information_barrier_segment_members.create_shield_information_barrier_segment_member(
            CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegment(
                id=segment.id,
                type=CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT,
            ),
            UserBase(id=get_env_var('USER_ID')),
        )
    )
    assert segment_member.user.id == get_env_var('USER_ID')
    assert segment_member.shield_information_barrier_segment.id == segment.id
    segment_members: ShieldInformationBarrierSegmentMembers = (
        client.shield_information_barrier_segment_members.get_shield_information_barrier_segment_members(
            segment.id
        )
    )
    assert len(segment_members.entries) > 0
    segment_member_get: ShieldInformationBarrierSegmentMember = (
        client.shield_information_barrier_segment_members.get_shield_information_barrier_segment_member_by_id(
            segment_member.id
        )
    )
    assert segment_member_get.id == segment_member.id
    client.shield_information_barrier_segment_members.delete_shield_information_barrier_segment_member_by_id(
        segment_member.id
    )
    with pytest.raises(Exception):
        client.shield_information_barrier_segment_members.get_shield_information_barrier_segment_member_by_id(
            segment_member.id
        )
    client.shield_information_barrier_segments.delete_shield_information_barrier_segment_by_id(
        segment.id
    )
