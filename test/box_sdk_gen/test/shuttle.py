from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2026_r0.shuttle_system_v2026_r0 import ShuttleSystemV2026R0

from box_sdk_gen.managers.shuttle import CreateShuttleSystemV2026R0SystemType

from box_sdk_gen.schemas.v2026_r0.shuttle_systems_v2026_r0 import ShuttleSystemsV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_agent_credentials_v2026_r0 import (
    ShuttleAgentCredentialsV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_jobs_v2026_r0 import ShuttleJobsV2026R0

from box_sdk_gen.managers.shuttle import CreateShuttleJobV2026R0JobType

from box_sdk_gen.schemas.v2026_r0.shuttle_runs_v2026_r0 import ShuttleRunsV2026R0

from box_sdk_gen.managers.shuttle import GetShuttlePathEntriesV2026R0Side

from box_sdk_gen.managers.shuttle import CreateShuttleReportV2026R0Format

from box_sdk_gen.managers.shuttle import UpdateShuttleJobScheduleByIdV2026R0RunMode

from box_sdk_gen.managers.shuttle import CreateShuttleJobScheduleV2026R0RunMode

from box_sdk_gen.managers.shuttle import CreateShuttleJobScheduleV2026R0State

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_time_v2026_r0 import (
    ShuttleJobScheduleTriggerByTimeV2026R0TypeField,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_time_v2026_r0 import (
    ShuttleJobScheduleTriggerByTimeV2026R0RepeatField,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationInputV2026R0TypeField,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_input_v2026_r0 import (
    ShuttlePathMappingAccountInputV2026R0,
)

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_time_v2026_r0 import (
    ShuttleJobScheduleTriggerByTimeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationInputV2026R0,
)

client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testCreateGetUpdateListDeleteShuttleSystemV2026R0():
    system_name: str = get_uuid()
    created_system: ShuttleSystemV2026R0 = (
        client.shuttle.create_shuttle_system_v2026_r0(
            system_name, system_type=CreateShuttleSystemV2026R0SystemType.WINDOWS
        )
    )
    assert created_system.name == system_name
    assert created_system.system_type == 'windows'
    assert to_string(created_system.type) == 'shuttle_system'
    system_from_api: ShuttleSystemV2026R0 = (
        client.shuttle.get_shuttle_system_by_id_v2026_r0(created_system.id)
    )
    assert system_from_api.id == created_system.id
    assert system_from_api.name == system_name
    updated_system_name: str = get_uuid()
    updated_system: ShuttleSystemV2026R0 = (
        client.shuttle.update_shuttle_system_by_id_v2026_r0(
            created_system.id, name=updated_system_name
        )
    )
    assert updated_system.name == updated_system_name
    systems: ShuttleSystemsV2026R0 = client.shuttle.get_shuttle_systems_v2026_r0()
    assert len(systems.entries) > 0
    credentials: ShuttleAgentCredentialsV2026R0 = (
        client.shuttle.create_shuttle_system_issue_registration_token_v2026_r0(
            created_system.id
        )
    )
    assert not credentials.registration_token == ''
    client.shuttle.delete_shuttle_system_by_id_v2026_r0(created_system.id)
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_system_by_id_v2026_r0(created_system.id)


def testShuttleJobsWithNonExistentIdV2026R0():
    resource_id: str = '123456'
    jobs: ShuttleJobsV2026R0 = client.shuttle.get_shuttle_jobs_v2026_r0()
    assert len(jobs.entries) >= 0
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_job_v2026_r0(
            get_uuid(), CreateShuttleJobV2026R0JobType.TRANSFER, resource_id
        )
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_job_by_id_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.update_shuttle_job_by_id_v2026_r0(resource_id, name=get_uuid())
    with pytest.raises(Exception):
        client.shuttle.delete_shuttle_job_by_id_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_job_start_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_job_stop_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_job_prepare_migration_v2026_r0(resource_id)


def testShuttleRunsWithNonExistentIdV2026R0():
    resource_id: str = '123456'
    runs: ShuttleRunsV2026R0 = client.shuttle.get_shuttle_runs_v2026_r0(resource_id)
    assert len(runs.entries) >= 0
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_run_by_id_v2026_r0(resource_id)


def testShuttleMappingsWithNonExistentIdV2026R0():
    resource_id: str = '123456'
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_path_mappings_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_path_mapping_by_id_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.update_shuttle_path_mapping_by_id_v2026_r0(
            resource_id, is_path_skipped=True
        )
    with pytest.raises(Exception):
        client.shuttle.delete_shuttle_path_mapping_by_id_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_path_mapping_import_v2026_r0(
            resource_id, resource_id
        )
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_subject_mappings_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_subject_mapping_v2026_r0(resource_id, resource_id)
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_subject_mapping_by_id_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.update_shuttle_subject_mapping_by_id_v2026_r0(
            resource_id, is_subject_skipped=True
        )
    with pytest.raises(Exception):
        client.shuttle.delete_shuttle_subject_mapping_by_id_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_subject_mapping_import_v2026_r0(
            resource_id, resource_id
        )
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_discovered_subjects_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_path_entries_v2026_r0(
            resource_id, GetShuttlePathEntriesV2026R0Side.SOURCE
        )
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_mapping_errors_v2026_r0(resource_id)


def testShuttleReportsWithNonExistentIdV2026R0():
    resource_id: str = '123456'
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_reports_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_report_v2026_r0(
            resource_id, CreateShuttleReportV2026R0Format.CSV, ['summary']
        )
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_report_by_id_v2026_r0(resource_id)


def testShuttleJobSchedulesWithNonExistentIdV2026R0():
    resource_id: str = '123456'
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_job_schedules_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.get_shuttle_job_schedule_by_id_v2026_r0(resource_id)
    with pytest.raises(Exception):
        client.shuttle.update_shuttle_job_schedule_by_id_v2026_r0(
            resource_id, run_mode=UpdateShuttleJobScheduleByIdV2026R0RunMode.SIMULATION
        )
    with pytest.raises(Exception):
        client.shuttle.delete_shuttle_job_schedule_by_id_v2026_r0(resource_id)


def testCreateShuttleJobScheduleWithNonExistentIdV2026R0():
    resource_id: str = '123456'
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_job_schedule_v2026_r0(
            resource_id,
            CreateShuttleJobScheduleV2026R0RunMode.TRANSFER,
            ShuttleJobScheduleTriggerByTimeV2026R0(
                type=ShuttleJobScheduleTriggerByTimeV2026R0TypeField.BY_TIME,
                start_at='2030-01-01T09:00:00',
                time_zone='America/Los_Angeles',
                repeat=ShuttleJobScheduleTriggerByTimeV2026R0RepeatField.DAILY,
            ),
            state=CreateShuttleJobScheduleV2026R0State.PAUSED,
        )


def testCreateShuttlePathMappingWithNonExistentIdV2026R0():
    resource_id: str = '123456'
    with pytest.raises(Exception):
        client.shuttle.create_shuttle_path_mapping_v2026_r0(
            resource_id,
            ShuttlePathMappingAccountLocationInputV2026R0(
                type=ShuttlePathMappingAccountLocationInputV2026R0TypeField.ACCOUNT,
                path='/finance',
                account=ShuttlePathMappingAccountInputV2026R0(email='user@example.com'),
            ),
        )
