from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.schemas.shield_information_barrier import ShieldInformationBarrier

from box_sdk_gen.schemas.shield_information_barrier_reports import (
    ShieldInformationBarrierReports,
)

from box_sdk_gen.schemas.shield_information_barrier_report import (
    ShieldInformationBarrierReport,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBaseTypeField,
)

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from test.box_sdk_gen.test.commons import get_or_create_shield_information_barrier

from box_sdk_gen.client import BoxClient


def testShieldInformationBarrierReports():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    barrier: ShieldInformationBarrier = get_or_create_shield_information_barrier(
        client, enterprise_id
    )
    assert to_string(barrier.status) == 'draft'
    assert to_string(barrier.type) == 'shield_information_barrier'
    assert barrier.enterprise.id == enterprise_id
    assert to_string(barrier.enterprise.type) == 'enterprise'
    barrier_id: str = barrier.id
    existing_reports: ShieldInformationBarrierReports = (
        client.shield_information_barrier_reports.get_shield_information_barrier_reports(
            barrier_id
        )
    )
    if len(existing_reports.entries) > 0:
        return None
    created_report: ShieldInformationBarrierReport = (
        client.shield_information_barrier_reports.create_shield_information_barrier_report(
            shield_information_barrier=ShieldInformationBarrierBase(
                id=barrier_id,
                type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER,
            )
        )
    )
    assert (
        created_report.shield_information_barrier.shield_information_barrier.id
        == barrier_id
    )
    retrieved_report: ShieldInformationBarrierReport = (
        client.shield_information_barrier_reports.get_shield_information_barrier_report_by_id(
            created_report.id
        )
    )
    assert retrieved_report.id == created_report.id
    retrieved_reports: ShieldInformationBarrierReports = (
        client.shield_information_barrier_reports.get_shield_information_barrier_reports(
            barrier_id
        )
    )
    assert len(retrieved_reports.entries) > 0
