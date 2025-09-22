from box_sdk_gen.internal.utils import to_string

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

from box_sdk_gen.schemas.shield_information_barrier_segments import (
    ShieldInformationBarrierSegments,
)

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from test.box_sdk_gen.test.commons import get_or_create_shield_information_barrier


def testShieldInformationBarrierSegments():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    barrier: ShieldInformationBarrier = get_or_create_shield_information_barrier(
        client, enterprise_id
    )
    barrier_id: str = barrier.id
    segment_name: str = get_uuid()
    segment_description: str = 'barrier segment description'
    segment: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.create_shield_information_barrier_segment(
            ShieldInformationBarrierBase(
                id=barrier_id,
                type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER,
            ),
            segment_name,
            description=segment_description,
        )
    )
    assert segment.name == segment_name
    segments: ShieldInformationBarrierSegments = (
        client.shield_information_barrier_segments.get_shield_information_barrier_segments(
            barrier_id
        )
    )
    assert len(segments.entries) > 0
    segment_id: str = segment.id
    segment_from_api: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.get_shield_information_barrier_segment_by_id(
            segment_id
        )
    )
    assert to_string(segment_from_api.type) == 'shield_information_barrier_segment'
    assert segment_from_api.id == segment_id
    assert segment_from_api.name == segment_name
    assert segment_from_api.description == segment_description
    assert segment_from_api.shield_information_barrier.id == barrier_id
    updated_segment_description: str = 'updated barrier segment description'
    updated_segment: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.update_shield_information_barrier_segment_by_id(
            segment_id, description=updated_segment_description
        )
    )
    assert updated_segment.description == updated_segment_description
    client.shield_information_barrier_segments.delete_shield_information_barrier_segment_by_id(
        segment_id
    )
    with pytest.raises(Exception):
        client.shield_information_barrier_segments.get_shield_information_barrier_segment_by_id(
            segment_id
        )
