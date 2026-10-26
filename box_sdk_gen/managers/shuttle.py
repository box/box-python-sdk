from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from typing import List

from box_sdk_gen.internal.null_value import NullValue

from typing import Union

from box_sdk_gen.schemas.v2026_r0.shuttle_job_permission_conflict_strategy_v2026_r0 import (
    ShuttleJobPermissionConflictStrategyV2026R0,
)

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_time_v2026_r0 import (
    ShuttleJobScheduleTriggerByTimeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_job_v2026_r0 import (
    ShuttleJobScheduleTriggerByJobV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_v2026_r0 import (
    ShuttleJobScheduleTriggerV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_input_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_location_input_v2026_r0 import (
    ShuttlePathMappingLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_target_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationTargetInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_target_input_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationTargetInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_target_location_input_v2026_r0 import (
    ShuttlePathMappingTargetLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_target_subject_input_v2026_r0 import (
    ShuttleTargetSubjectInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_systems_v2026_r0 import ShuttleSystemsV2026R0

from box_sdk_gen.schemas.v2026_r0.client_error_v2026_r0 import ClientErrorV2026R0

from box_sdk_gen.parameters.v2026_r0.box_version_header_v2026_r0 import (
    BoxVersionHeaderV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_system_v2026_r0 import ShuttleSystemV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_system_create_request_v2026_r0 import (
    ShuttleSystemCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_system_update_request_v2026_r0 import (
    ShuttleSystemUpdateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_agent_credentials_v2026_r0 import (
    ShuttleAgentCredentialsV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_jobs_v2026_r0 import ShuttleJobsV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_job_v2026_r0 import ShuttleJobV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_job_create_request_v2026_r0 import (
    ShuttleJobCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_update_request_v2026_r0 import (
    ShuttleJobUpdateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_start_request_v2026_r0 import (
    ShuttleJobStartRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_runs_v2026_r0 import ShuttleRunsV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_run_v2026_r0 import ShuttleRunV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedules_v2026_r0 import (
    ShuttleJobSchedulesV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_v2026_r0 import (
    ShuttleJobScheduleV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_create_request_v2026_r0 import (
    ShuttleJobScheduleCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_update_request_v2026_r0 import (
    ShuttleJobScheduleUpdateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mappings_v2026_r0 import (
    ShuttlePathMappingsV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_v2026_r0 import (
    ShuttlePathMappingV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_create_request_v2026_r0 import (
    ShuttlePathMappingCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_update_request_v2026_r0 import (
    ShuttlePathMappingUpdateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_import_create_request_v2026_r0 import (
    ShuttlePathMappingImportCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_mapping_import_create_request_v2026_r0 import (
    ShuttleSubjectMappingImportCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_mappings_v2026_r0 import (
    ShuttleSubjectMappingsV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_mapping_v2026_r0 import (
    ShuttleSubjectMappingV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_mapping_create_request_v2026_r0 import (
    ShuttleSubjectMappingCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_mapping_update_request_v2026_r0 import (
    ShuttleSubjectMappingUpdateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_discovered_subjects_v2026_r0 import (
    ShuttleDiscoveredSubjectsV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_entries_v2026_r0 import (
    ShuttlePathEntriesV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_mapping_errors_v2026_r0 import (
    ShuttleMappingErrorsV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_reports_v2026_r0 import ShuttleReportsV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_report_v2026_r0 import ShuttleReportV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_report_create_request_v2026_r0 import (
    ShuttleReportCreateRequestV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class CreateShuttleSystemV2026R0SystemType(str, Enum):
    WINDOWS = 'windows'


class CreateShuttleJobV2026R0JobType(str, Enum):
    TRANSFER = 'transfer'
    ANALYSIS = 'analysis'


class CreateShuttleJobV2026R0AccountMapping(BaseObject):
    def __init__(
        self,
        *,
        is_enabled: Optional[bool] = None,
        permission_conflict_strategy: Optional[
            ShuttleJobPermissionConflictStrategyV2026R0
        ] = None,
        are_external_shares_mapped: Optional[bool] = None,
        are_permissions_mapped: Optional[bool] = None,
        **kwargs
    ):
        """
                :param is_enabled: Whether account mapping is enabled for the shuttle job. Defaults to
        `false` when `account_mapping` is omitted on create., defaults to None
                :type is_enabled: Optional[bool], optional
                :param permission_conflict_strategy: The strategy used to resolve permission conflicts. `null` when
        unset., defaults to None
                :type permission_conflict_strategy: Optional[ShuttleJobPermissionConflictStrategyV2026R0], optional
                :param are_external_shares_mapped: Whether external shares are mapped during the migration., defaults to None
                :type are_external_shares_mapped: Optional[bool], optional
                :param are_permissions_mapped: Whether permissions are mapped during the migration., defaults to None
                :type are_permissions_mapped: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.is_enabled = is_enabled
        self.permission_conflict_strategy = permission_conflict_strategy
        self.are_external_shares_mapped = are_external_shares_mapped
        self.are_permissions_mapped = are_permissions_mapped


class CreateShuttleJobV2026R0Settings(BaseObject):
    def __init__(
        self,
        *,
        bandwidth_limit_bytes_per_sec: Optional[int] = None,
        are_deletions_mirrored: Optional[bool] = None,
        are_file_versions_synced: Optional[bool] = None,
        max_file_versions: Optional[int] = None,
        is_overwrite_enabled: Optional[bool] = None,
        are_completed_mappings_skipped_on_rerun: Optional[bool] = None,
        is_content_scanning_enabled: Optional[bool] = None,
        include_shared_source_folders: Optional[bool] = None,
        include_shared_destination_folders: Optional[bool] = None,
        **kwargs
    ):
        """
                :param bandwidth_limit_bytes_per_sec: The maximum transfer bandwidth in bytes per second. `null` when
        unlimited., defaults to None
                :type bandwidth_limit_bytes_per_sec: Optional[int], optional
                :param are_deletions_mirrored: Whether deletions in the source system are mirrored in Box., defaults to None
                :type are_deletions_mirrored: Optional[bool], optional
                :param are_file_versions_synced: Whether prior file versions are synced during the migration., defaults to None
                :type are_file_versions_synced: Optional[bool], optional
                :param max_file_versions: The maximum number of file versions to sync. `null` when unlimited., defaults to None
                :type max_file_versions: Optional[int], optional
                :param is_overwrite_enabled: Whether existing files in Box are overwritten., defaults to None
                :type is_overwrite_enabled: Optional[bool], optional
                :param are_completed_mappings_skipped_on_rerun: Whether mappings that already completed successfully are skipped when
        the job is rerun., defaults to None
                :type are_completed_mappings_skipped_on_rerun: Optional[bool], optional
                :param is_content_scanning_enabled: Whether migrated content is scanned during the migration. Applies
        only when the source system supports content scanning; ignored
        otherwise., defaults to None
                :type is_content_scanning_enabled: Optional[bool], optional
                :param include_shared_source_folders: Whether shared folders on the source are included in the migration.
        Applies only when the source system supports shared folders; ignored
        otherwise., defaults to None
                :type include_shared_source_folders: Optional[bool], optional
                :param include_shared_destination_folders: Whether shared folders on the destination are included in the
        migration. Applies only when the destination system supports shared
        folders; ignored otherwise., defaults to None
                :type include_shared_destination_folders: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.bandwidth_limit_bytes_per_sec = bandwidth_limit_bytes_per_sec
        self.are_deletions_mirrored = are_deletions_mirrored
        self.are_file_versions_synced = are_file_versions_synced
        self.max_file_versions = max_file_versions
        self.is_overwrite_enabled = is_overwrite_enabled
        self.are_completed_mappings_skipped_on_rerun = (
            are_completed_mappings_skipped_on_rerun
        )
        self.is_content_scanning_enabled = is_content_scanning_enabled
        self.include_shared_source_folders = include_shared_source_folders
        self.include_shared_destination_folders = include_shared_destination_folders


class UpdateShuttleJobByIdV2026R0AccountMapping(BaseObject):
    def __init__(
        self,
        *,
        is_enabled: Optional[bool] = None,
        permission_conflict_strategy: Optional[
            ShuttleJobPermissionConflictStrategyV2026R0
        ] = None,
        are_external_shares_mapped: Optional[bool] = None,
        are_permissions_mapped: Optional[bool] = None,
        **kwargs
    ):
        """
                :param is_enabled: Whether account mapping is enabled for the shuttle job., defaults to None
                :type is_enabled: Optional[bool], optional
                :param permission_conflict_strategy: The strategy used to resolve permission conflicts. `null` when
        unset., defaults to None
                :type permission_conflict_strategy: Optional[ShuttleJobPermissionConflictStrategyV2026R0], optional
                :param are_external_shares_mapped: Whether external shares are mapped during the migration., defaults to None
                :type are_external_shares_mapped: Optional[bool], optional
                :param are_permissions_mapped: Whether permissions are mapped during the migration., defaults to None
                :type are_permissions_mapped: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.is_enabled = is_enabled
        self.permission_conflict_strategy = permission_conflict_strategy
        self.are_external_shares_mapped = are_external_shares_mapped
        self.are_permissions_mapped = are_permissions_mapped


class UpdateShuttleJobByIdV2026R0Settings(BaseObject):
    def __init__(
        self,
        *,
        bandwidth_limit_bytes_per_sec: Optional[int] = None,
        are_deletions_mirrored: Optional[bool] = None,
        are_file_versions_synced: Optional[bool] = None,
        max_file_versions: Optional[int] = None,
        is_overwrite_enabled: Optional[bool] = None,
        are_completed_mappings_skipped_on_rerun: Optional[bool] = None,
        is_content_scanning_enabled: Optional[bool] = None,
        include_shared_source_folders: Optional[bool] = None,
        include_shared_destination_folders: Optional[bool] = None,
        **kwargs
    ):
        """
                :param bandwidth_limit_bytes_per_sec: The maximum transfer bandwidth in bytes per second. `null` when
        unlimited., defaults to None
                :type bandwidth_limit_bytes_per_sec: Optional[int], optional
                :param are_deletions_mirrored: Whether deletions in the source system are mirrored in Box., defaults to None
                :type are_deletions_mirrored: Optional[bool], optional
                :param are_file_versions_synced: Whether prior file versions are synced during the migration., defaults to None
                :type are_file_versions_synced: Optional[bool], optional
                :param max_file_versions: The maximum number of file versions to sync. `null` when unlimited., defaults to None
                :type max_file_versions: Optional[int], optional
                :param is_overwrite_enabled: Whether existing files in Box are overwritten., defaults to None
                :type is_overwrite_enabled: Optional[bool], optional
                :param are_completed_mappings_skipped_on_rerun: Whether mappings that already completed successfully are skipped when
        the job is rerun., defaults to None
                :type are_completed_mappings_skipped_on_rerun: Optional[bool], optional
                :param is_content_scanning_enabled: Whether migrated content is scanned during the migration. Applies
        only when the source system supports content scanning; ignored
        otherwise., defaults to None
                :type is_content_scanning_enabled: Optional[bool], optional
                :param include_shared_source_folders: Whether shared folders on the source are included in the migration.
        Applies only when the source system supports shared folders; ignored
        otherwise., defaults to None
                :type include_shared_source_folders: Optional[bool], optional
                :param include_shared_destination_folders: Whether shared folders on the destination are included in the
        migration. Applies only when the destination system supports shared
        folders; ignored otherwise., defaults to None
                :type include_shared_destination_folders: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.bandwidth_limit_bytes_per_sec = bandwidth_limit_bytes_per_sec
        self.are_deletions_mirrored = are_deletions_mirrored
        self.are_file_versions_synced = are_file_versions_synced
        self.max_file_versions = max_file_versions
        self.is_overwrite_enabled = is_overwrite_enabled
        self.are_completed_mappings_skipped_on_rerun = (
            are_completed_mappings_skipped_on_rerun
        )
        self.is_content_scanning_enabled = is_content_scanning_enabled
        self.include_shared_source_folders = include_shared_source_folders
        self.include_shared_destination_folders = include_shared_destination_folders


class CreateShuttleJobStartV2026R0Mode(str, Enum):
    TRANSFER = 'transfer'
    SIMULATION = 'simulation'
    SCAN = 'scan'
    ANALYSIS = 'analysis'


class CreateShuttleJobScheduleV2026R0RunMode(str, Enum):
    TRANSFER = 'transfer'
    SIMULATION = 'simulation'
    ANALYSIS = 'analysis'


class CreateShuttleJobScheduleV2026R0State(str, Enum):
    ENABLED = 'enabled'
    PAUSED = 'paused'


class UpdateShuttleJobScheduleByIdV2026R0State(str, Enum):
    ENABLED = 'enabled'
    PAUSED = 'paused'


class UpdateShuttleJobScheduleByIdV2026R0RunMode(str, Enum):
    TRANSFER = 'transfer'
    SIMULATION = 'simulation'
    ANALYSIS = 'analysis'


class GetShuttlePathEntriesV2026R0Side(str, Enum):
    SOURCE = 'source'
    TARGET = 'target'


class CreateShuttleReportV2026R0Format(str, Enum):
    XLSX = 'xlsx'
    CSV = 'csv'


class CreateShuttleReportV2026R0UsersScope(str, Enum):
    MIGRATED = 'migrated'
    ALL = 'all'


class ShuttleManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: Optional[NetworkSession] = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_shuttle_systems_v2026_r0(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSystemsV2026R0:
        """
                Returns a paginated list of shuttle systems accessible to the

                authenticated user.

                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'marker': to_string(marker), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shuttle_systems']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSystemsV2026R0)

    def create_shuttle_system_v2026_r0(
        self,
        name: str,
        *,
        system_type: CreateShuttleSystemV2026R0SystemType = CreateShuttleSystemV2026R0SystemType.WINDOWS,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSystemV2026R0:
        """
                Creates a new shuttle system. Only Windows agent systems can be created

                through the public API; other system types must be configured through the


                Shuttle application.

                :param name: The display name for the new shuttle system.
                :type name: str
                :param system_type: The public system type identifier for the new shuttle system. Only
        `windows` is currently supported through the public API., defaults to CreateShuttleSystemV2026R0SystemType.WINDOWS
                :type system_type: CreateShuttleSystemV2026R0SystemType, optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'name': name, 'system_type': system_type}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shuttle_systems']
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSystemV2026R0)

    def get_shuttle_system_by_id_v2026_r0(
        self,
        shuttle_system_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSystemV2026R0:
        """
                Returns details for a single shuttle system identified by its ID,

                including its type and connection state.

                :param shuttle_system_id: The unique identifier for the shuttle system.
        Example: "6a315c0754833bfc5df067bf"
                :type shuttle_system_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_systems/',
                        to_string(shuttle_system_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSystemV2026R0)

    def update_shuttle_system_by_id_v2026_r0(
        self,
        shuttle_system_id: str,
        *,
        name: Optional[str] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSystemV2026R0:
        """
                Updates the mutable properties of an existing shuttle system identified by

                its ID. Only the fields supplied in the request body are changed.

                :param shuttle_system_id: The unique identifier for the shuttle system.
        Example: "6a315c0754833bfc5df067bf"
                :type shuttle_system_id: str
                :param name: The updated display name for the shuttle system., defaults to None
                :type name: Optional[str], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'name': name}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_systems/',
                        to_string(shuttle_system_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSystemV2026R0)

    def delete_shuttle_system_by_id_v2026_r0(
        self,
        shuttle_system_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Permanently deletes the shuttle system identified by its ID. This does not

                affect content that has already been migrated.

                :param shuttle_system_id: The unique identifier for the shuttle system.
        Example: "6a315c0754833bfc5df067bf"
                :type shuttle_system_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_systems/',
                        to_string(shuttle_system_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def create_shuttle_system_issue_registration_token_v2026_r0(
        self,
        shuttle_system_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleAgentCredentialsV2026R0:
        """
                Issues a new installation token for the Windows shuttle system identified

                by its ID. Paste the returned token into the Windows agent installer to


                register the agent with this system.

                :param shuttle_system_id: The unique identifier for the shuttle system.
        Example: "6a315c0754833bfc5df067bf"
                :type shuttle_system_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_systems/',
                        to_string(shuttle_system_id),
                        '/issue_registration_token',
                    ]
                ),
                method='POST',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleAgentCredentialsV2026R0)

    def get_shuttle_jobs_v2026_r0(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobsV2026R0:
        """
                Returns a paginated list of shuttle jobs accessible to the authenticated

                user.

                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'marker': to_string(marker), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shuttle_jobs']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobsV2026R0)

    def create_shuttle_job_v2026_r0(
        self,
        name: str,
        job_type: CreateShuttleJobV2026R0JobType,
        source_system_id: str,
        *,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        account_mapping: Optional[CreateShuttleJobV2026R0AccountMapping] = None,
        settings: Optional[CreateShuttleJobV2026R0Settings] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobV2026R0:
        """
                Creates a new shuttle job that describes a migration from the given source

                system into Box.

                :param name: The human-readable name of the shuttle job.
                :type name: str
                :param job_type: The type of work the shuttle job performs.
                :type job_type: CreateShuttleJobV2026R0JobType
                :param source_system_id: The unique identifier of the source system to migrate from.
                :type source_system_id: str
                :param comment: An optional free-form comment describing the shuttle job., defaults to None
                :type comment: Optional[str], optional
                :param tags: A list of free-form tags associated with the shuttle job., defaults to None
                :type tags: Optional[List[str]], optional
                :param account_mapping: The account mapping configuration that controls how source identities
        and permissions are translated into Box. When this object is omitted,
        the job is created with `is_enabled` set to `false`., defaults to None
                :type account_mapping: Optional[CreateShuttleJobV2026R0AccountMapping], optional
                :param settings: The tunable settings that control how the shuttle job runs., defaults to None
                :type settings: Optional[CreateShuttleJobV2026R0Settings], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'name': name,
            'job_type': job_type,
            'source_system_id': source_system_id,
            'comment': comment,
            'tags': tags,
            'account_mapping': account_mapping,
            'settings': settings,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shuttle_jobs']
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobV2026R0)

    def get_shuttle_job_by_id_v2026_r0(
        self,
        shuttle_job_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobV2026R0:
        """
                Returns details for a single shuttle job identified by its ID, including

                its current state, mapping-preparation state, and configured source system.

                :param shuttle_job_id: The unique identifier for the shuttle job.
        Example: "6a3ba68e810d9156194530a1"
                :type shuttle_job_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_jobs/',
                        to_string(shuttle_job_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobV2026R0)

    def update_shuttle_job_by_id_v2026_r0(
        self,
        shuttle_job_id: str,
        *,
        name: Optional[str] = None,
        comment: Union[Optional[str], NullValue] = None,
        tags: Optional[List[str]] = None,
        account_mapping: Optional[UpdateShuttleJobByIdV2026R0AccountMapping] = None,
        settings: Optional[UpdateShuttleJobByIdV2026R0Settings] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobV2026R0:
        """
                Updates the mutable properties of an existing shuttle job identified by its

                ID. Only the fields supplied in the request body are changed.

                :param shuttle_job_id: The unique identifier for the shuttle job.
        Example: "6a3ba68e810d9156194530a1"
                :type shuttle_job_id: str
                :param name: The human-readable name of the shuttle job., defaults to None
                :type name: Optional[str], optional
                :param comment: An optional free-form comment describing the shuttle job., defaults to None
                :type comment: Union[Optional[str], NullValue], optional
                :param tags: A list of free-form tags associated with the shuttle job., defaults to None
                :type tags: Optional[List[str]], optional
                :param account_mapping: The account mapping configuration that controls how source identities
        and permissions are translated into Box., defaults to None
                :type account_mapping: Optional[UpdateShuttleJobByIdV2026R0AccountMapping], optional
                :param settings: The tunable settings that control how the shuttle job runs., defaults to None
                :type settings: Optional[UpdateShuttleJobByIdV2026R0Settings], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'name': name,
            'comment': comment,
            'tags': tags,
            'account_mapping': account_mapping,
            'settings': settings,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_jobs/',
                        to_string(shuttle_job_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobV2026R0)

    def delete_shuttle_job_by_id_v2026_r0(
        self,
        shuttle_job_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Permanently deletes the shuttle job identified by its ID. This does not

                affect content that has already been migrated.

                :param shuttle_job_id: The unique identifier for the shuttle job.
        Example: "6a3ba68e810d9156194530a1"
                :type shuttle_job_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_jobs/',
                        to_string(shuttle_job_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def create_shuttle_job_start_v2026_r0(
        self,
        shuttle_job_id: str,
        *,
        mode: Optional[CreateShuttleJobStartV2026R0Mode] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Starts the job in the given mode. When no body is provided the job runs in

                simulation mode.

                :param shuttle_job_id: The unique identifier for the shuttle job.
        Example: "6a3ba68e810d9156194530a1"
                :type shuttle_job_id: str
                :param mode: The run mode. Defaults to simulation when omitted., defaults to None
                :type mode: Optional[CreateShuttleJobStartV2026R0Mode], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'mode': mode}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_jobs/',
                        to_string(shuttle_job_id),
                        '/start',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body) if not request_body == None else None,
                content_type='application/json',
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def create_shuttle_job_stop_v2026_r0(
        self,
        shuttle_job_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Stops a running shuttle job identified by its ID. Any work already in

                progress is allowed to finish before the job transitions to a stopped


                state.

                :param shuttle_job_id: The unique identifier for the shuttle job.
        Example: "6a3ba68e810d9156194530a1"
                :type shuttle_job_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_jobs/',
                        to_string(shuttle_job_id),
                        '/stop',
                    ]
                ),
                method='POST',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def create_shuttle_job_prepare_migration_v2026_r0(
        self,
        shuttle_job_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Validates the configured account and path mappings before a transfer. Only

                relevant when account mapping is enabled.

                :param shuttle_job_id: The unique identifier for the shuttle job.
        Example: "6a3ba68e810d9156194530a1"
                :type shuttle_job_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_jobs/',
                        to_string(shuttle_job_id),
                        '/prepare_migration',
                    ]
                ),
                method='POST',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def get_shuttle_runs_v2026_r0(
        self,
        job_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleRunsV2026R0:
        """
                Returns a paginated list of runs for the shuttle job identified by

                `job_id`.

                :param job_id: The unique identifier of the shuttle job whose runs to list.
                :type job_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'job_id': to_string(job_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shuttle_runs']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleRunsV2026R0)

    def get_shuttle_run_by_id_v2026_r0(
        self,
        shuttle_run_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleRunV2026R0:
        """
                Returns details for a single shuttle run identified by its ID, including

                its mode, state, timing, and transfer statistics.

                :param shuttle_run_id: The unique identifier for the shuttle run, in the form
        `{job_id}:{run_number}`.
        Example: "6a3ba68e810d9156194530a1:42"
                :type shuttle_run_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_runs/',
                        to_string(shuttle_run_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleRunV2026R0)

    def get_shuttle_job_schedules_v2026_r0(
        self,
        job_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobSchedulesV2026R0:
        """
                Returns a paginated list of schedules for the shuttle job identified by

                `job_id`.

                :param job_id: The unique identifier of the shuttle job whose schedules to list.
                :type job_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'job_id': to_string(job_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_job_schedules',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobSchedulesV2026R0)

    def create_shuttle_job_schedule_v2026_r0(
        self,
        job_id: str,
        run_mode: CreateShuttleJobScheduleV2026R0RunMode,
        trigger: ShuttleJobScheduleTriggerV2026R0,
        *,
        state: Optional[CreateShuttleJobScheduleV2026R0State] = None,
        description: Union[Optional[str], NullValue] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobScheduleV2026R0:
        """
                Creates a schedule that starts runs of the shuttle job identified by

                `job_id`. The schedule starts a run either at a wall-clock time or after


                another job's run meets a condition. Schedules cannot start a run in


                `scan` mode.

                :param job_id: The unique identifier of the shuttle job this schedule belongs to.
                :type job_id: str
                :param run_mode: The kind of run the schedule starts. `scan` is not a valid schedule
        run mode.
                :type run_mode: CreateShuttleJobScheduleV2026R0RunMode
                :param state: Whether the schedule is active. When omitted, defaults to `enabled`., defaults to None
                :type state: Optional[CreateShuttleJobScheduleV2026R0State], optional
                :param description: An optional human-readable description of the schedule., defaults to None
                :type description: Union[Optional[str], NullValue], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'job_id': job_id,
            'run_mode': run_mode,
            'state': state,
            'description': description,
            'trigger': trigger,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_job_schedules',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobScheduleV2026R0)

    def get_shuttle_job_schedule_by_id_v2026_r0(
        self,
        shuttle_job_schedule_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobScheduleV2026R0:
        """
                Retrieves the shuttle job schedule identified by its ID.
                :param shuttle_job_schedule_id: The unique identifier for the shuttle job schedule.
        Example: "7c1ba68e810d9156194530b2"
                :type shuttle_job_schedule_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_job_schedules/',
                        to_string(shuttle_job_schedule_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobScheduleV2026R0)

    def update_shuttle_job_schedule_by_id_v2026_r0(
        self,
        shuttle_job_schedule_id: str,
        *,
        state: Optional[UpdateShuttleJobScheduleByIdV2026R0State] = None,
        run_mode: Optional[UpdateShuttleJobScheduleByIdV2026R0RunMode] = None,
        description: Union[Optional[str], NullValue] = None,
        trigger: Optional[ShuttleJobScheduleTriggerV2026R0] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleJobScheduleV2026R0:
        """
                Updates the mutable properties of an existing shuttle job schedule

                identified by its ID. Only the fields supplied in the request body are


                changed. The owning job cannot be changed.

                :param shuttle_job_schedule_id: The unique identifier for the shuttle job schedule.
        Example: "7c1ba68e810d9156194530b2"
                :type shuttle_job_schedule_id: str
                :param state: Whether the schedule is active., defaults to None
                :type state: Optional[UpdateShuttleJobScheduleByIdV2026R0State], optional
                :param run_mode: The kind of run the schedule starts. `scan` is not a valid schedule
        run mode., defaults to None
                :type run_mode: Optional[UpdateShuttleJobScheduleByIdV2026R0RunMode], optional
                :param description: An optional human-readable description of the schedule., defaults to None
                :type description: Union[Optional[str], NullValue], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'state': state,
            'run_mode': run_mode,
            'description': description,
            'trigger': trigger,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_job_schedules/',
                        to_string(shuttle_job_schedule_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleJobScheduleV2026R0)

    def delete_shuttle_job_schedule_by_id_v2026_r0(
        self,
        shuttle_job_schedule_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Permanently deletes the shuttle job schedule identified by its ID. This

                does not affect runs that have already started.

                :param shuttle_job_schedule_id: The unique identifier for the shuttle job schedule.
        Example: "7c1ba68e810d9156194530b2"
                :type shuttle_job_schedule_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_job_schedules/',
                        to_string(shuttle_job_schedule_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def get_shuttle_path_mappings_v2026_r0(
        self,
        job_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttlePathMappingsV2026R0:
        """
                Returns a paginated list of path mappings for the shuttle job identified

                by `job_id`.

                :param job_id: The unique identifier of the shuttle job whose path mappings to list.
                :type job_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'job_id': to_string(job_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_path_mappings',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttlePathMappingsV2026R0)

    def create_shuttle_path_mapping_v2026_r0(
        self,
        job_id: str,
        source: ShuttlePathMappingLocationInputV2026R0,
        *,
        is_path_skipped: Optional[bool] = None,
        target: Optional[ShuttlePathMappingTargetLocationInputV2026R0] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttlePathMappingV2026R0:
        """
                Creates a path mapping that connects a source location on the migrated

                system to a destination in Box for the given shuttle job.

                :param job_id: The unique identifier of the shuttle job this mapping belongs to.
                :type job_id: str
                :param is_path_skipped: Whether this source path should be skipped during the migration.
        Defaults to `false`., defaults to None
                :type is_path_skipped: Optional[bool], optional
                :param target: The destination location to migrate to. Omit or set to `null` when the
        source path is skipped., defaults to None
                :type target: Optional[ShuttlePathMappingTargetLocationInputV2026R0], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'job_id': job_id,
            'is_path_skipped': is_path_skipped,
            'source': source,
            'target': target,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_path_mappings',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttlePathMappingV2026R0)

    def get_shuttle_path_mapping_by_id_v2026_r0(
        self,
        shuttle_path_mapping_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttlePathMappingV2026R0:
        """
                Returns details for a single shuttle path mapping identified by its ID,

                including the source location and destination, if any.

                :param shuttle_path_mapping_id: The unique identifier for the shuttle path mapping.
        Example: "6a3ba7a24ea17bc9461eeacd"
                :type shuttle_path_mapping_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_path_mappings/',
                        to_string(shuttle_path_mapping_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttlePathMappingV2026R0)

    def update_shuttle_path_mapping_by_id_v2026_r0(
        self,
        shuttle_path_mapping_id: str,
        *,
        is_path_skipped: Optional[bool] = None,
        source: Optional[ShuttlePathMappingLocationInputV2026R0] = None,
        target: Optional[ShuttlePathMappingTargetLocationInputV2026R0] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttlePathMappingV2026R0:
        """
                Updates the mutable properties of an existing shuttle path mapping

                identified by its ID. Only the fields supplied in the request body are


                changed.

                :param shuttle_path_mapping_id: The unique identifier for the shuttle path mapping.
        Example: "6a3ba7a24ea17bc9461eeacd"
                :type shuttle_path_mapping_id: str
                :param is_path_skipped: Whether this source path should be skipped during the migration., defaults to None
                :type is_path_skipped: Optional[bool], optional
                :param target: The destination location to migrate to. Set to `null` to clear the
        destination, for example when skipping the source path., defaults to None
                :type target: Optional[ShuttlePathMappingTargetLocationInputV2026R0], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'is_path_skipped': is_path_skipped,
            'source': source,
            'target': target,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_path_mappings/',
                        to_string(shuttle_path_mapping_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttlePathMappingV2026R0)

    def delete_shuttle_path_mapping_by_id_v2026_r0(
        self,
        shuttle_path_mapping_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Permanently deletes the shuttle path mapping identified by its ID. This

                does not affect content that has already been migrated.

                :param shuttle_path_mapping_id: The unique identifier for the shuttle path mapping.
        Example: "6a3ba7a24ea17bc9461eeacd"
                :type shuttle_path_mapping_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_path_mappings/',
                        to_string(shuttle_path_mapping_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def create_shuttle_path_mapping_import_v2026_r0(
        self,
        job_id: str,
        file_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Accepts a spreadsheet of path mappings, already stored in Box, and replaces

                the job's path mappings.


                A file that is not a mapping workbook, or that exceeds the size or row


                limits (10 MiB Box download limit; 100,000 mapping rows), returns `400`


                synchronously and leaves the job unchanged.


                An accepted import always replaces every path mapping on the job. When all


                rows are valid the workbook is deployed in full. When any row is invalid


                the job ends with no path mappings and `mapping_state` becomes


                `paths_import_rejected` until the next import or the next manual


                path-mapping change. Row problems are listed by


                `GET /shuttle_mapping_errors?job_id=…` with category `path_import`, messages


                of the form `Row N: …`, at most 500 entries plus one overflow entry.


                Validation and deployment are asynchronous after acceptance. Poll


                `GET /shuttle_jobs/{shuttle_job_id}` while `mapping_state` is


                `importing_paths`. Only one import may be in flight per job.

                :param job_id: The unique identifier of the shuttle job whose path mappings are
        replaced.
                :type job_id: str
                :param file_id: The unique identifier of the Box file holding the mapping workbook. The
        file is read as the calling user, so it must live somewhere that user can
        download from.
                :type file_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'job_id': job_id, 'file_id': file_id}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_path_mapping_imports',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def create_shuttle_subject_mapping_import_v2026_r0(
        self,
        job_id: str,
        file_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Accepts a spreadsheet of subject (user and group) mappings, already stored

                in Box, and replaces the job's subject mappings.


                A file that is not a subject-mapping workbook, or that exceeds the size or


                row limits (10 MiB Box download limit; 50,000 mapping rows), returns `400`


                synchronously and leaves the job unchanged.


                An accepted import always replaces every subject mapping on the job. When


                all rows are valid the workbook is deployed in full. When any row is


                invalid the job ends with no subject mappings and `mapping_state` becomes


                `subjects_import_rejected` until the next import or the next manual


                subject-mapping change. Row problems are listed by


                `GET /shuttle_mapping_errors?job_id=…` with category `subject_import`,


                messages of the form `Row N: …`, at most 500 entries plus one overflow


                entry.


                Validation and deployment are asynchronous after acceptance. Poll


                `GET /shuttle_jobs/{shuttle_job_id}` while `mapping_state` is


                `importing_subjects`. Only one import may be in flight per job. The job


                must map subjects (`account_mapping` enabled) and its source scan must be


                finished; otherwise the request returns `409`.


                Expected workbook format (API clients cannot download the UI template):


                sheets `Users` and/or `Groups` (a sheet named `Subjects` is also accepted).


                Columns are `Source User <Key>`, `Target User <Key>`, `Skip` on `Users`,


                and `Source Group <Key>`, `Target Group <Key>`, `Skip` on `Groups`, where


                `<Key>` is the primary identifier for that role and system:


                - Users: `Email` for most systems; `ID` for `SharePoint` (2007/2010/2013);


                  `Name` for Windows (`windows_union`, stored as the user id).


                - Groups: `Name` for most systems; `Email` for Google Drive admin groups.


                Source rows for a template can be taken from


                `GET /shuttle_discovered_subjects`.

                :param job_id: The unique identifier of the shuttle job whose subject mappings are
        replaced.
                :type job_id: str
                :param file_id: The unique identifier of the Box file holding the mapping workbook. The
        file is read as the calling user, so it must live somewhere that user can
        download from.
                :type file_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'job_id': job_id, 'file_id': file_id}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_subject_mapping_imports',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def get_shuttle_subject_mappings_v2026_r0(
        self,
        job_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSubjectMappingsV2026R0:
        """
                Returns a paginated list of subject mappings for the shuttle job identified

                by `job_id`.

                :param job_id: The unique identifier of the shuttle job whose subject mappings to list.
                :type job_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'job_id': to_string(job_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_subject_mappings',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSubjectMappingsV2026R0)

    def create_shuttle_subject_mapping_v2026_r0(
        self,
        job_id: str,
        discovered_subject_id: str,
        *,
        revision: Optional[int] = None,
        is_subject_skipped: Optional[bool] = None,
        target: Optional[ShuttleTargetSubjectInputV2026R0] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSubjectMappingV2026R0:
        """
                Creates a subject mapping that connects a discovered source subject to a

                Box user or group for the given shuttle job.

                :param job_id: The unique identifier of the shuttle job this mapping belongs to.
                :type job_id: str
                :param discovered_subject_id: The unique identifier of the discovered subject to map.
                :type discovered_subject_id: str
                :param revision: The discovery-requirements revision to resolve against. Omit to use the
        latest revision., defaults to None
                :type revision: Optional[int], optional
                :param is_subject_skipped: Whether this subject should be skipped during the migration. Defaults
        to `false`., defaults to None
                :type is_subject_skipped: Optional[bool], optional
                :param target: The Box target to map to. Omit or set to `null` when the subject is
        skipped., defaults to None
                :type target: Optional[ShuttleTargetSubjectInputV2026R0], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'job_id': job_id,
            'discovered_subject_id': discovered_subject_id,
            'revision': revision,
            'is_subject_skipped': is_subject_skipped,
            'target': target,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_subject_mappings',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSubjectMappingV2026R0)

    def get_shuttle_subject_mapping_by_id_v2026_r0(
        self,
        shuttle_subject_mapping_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSubjectMappingV2026R0:
        """
                Returns details for a single shuttle subject mapping identified by its ID,

                including the source subject and Box target, if any.

                :param shuttle_subject_mapping_id: The unique identifier for the shuttle subject mapping.
        Example: "6a3ba7b12ea17bc9461eeace"
                :type shuttle_subject_mapping_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_subject_mappings/',
                        to_string(shuttle_subject_mapping_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSubjectMappingV2026R0)

    def update_shuttle_subject_mapping_by_id_v2026_r0(
        self,
        shuttle_subject_mapping_id: str,
        *,
        is_subject_skipped: Optional[bool] = None,
        target: Optional[ShuttleTargetSubjectInputV2026R0] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleSubjectMappingV2026R0:
        """
                Updates the mutable properties of an existing shuttle subject mapping

                identified by its ID. Only the fields supplied in the request body are


                changed.

                :param shuttle_subject_mapping_id: The unique identifier for the shuttle subject mapping.
        Example: "6a3ba7b12ea17bc9461eeace"
                :type shuttle_subject_mapping_id: str
                :param is_subject_skipped: Whether this subject should be skipped during the migration., defaults to None
                :type is_subject_skipped: Optional[bool], optional
                :param target: The Box target to map to. Set to `null` only for a skipped subject.
        Setting it to `null` while the mapping is active fails validation.
        Updating `is_subject_skipped` alone preserves the existing target., defaults to None
                :type target: Optional[ShuttleTargetSubjectInputV2026R0], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'is_subject_skipped': is_subject_skipped,
            'target': target,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_subject_mappings/',
                        to_string(shuttle_subject_mapping_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleSubjectMappingV2026R0)

    def delete_shuttle_subject_mapping_by_id_v2026_r0(
        self,
        shuttle_subject_mapping_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Permanently deletes the shuttle subject mapping identified by its ID.
                :param shuttle_subject_mapping_id: The unique identifier for the shuttle subject mapping.
        Example: "6a3ba7b12ea17bc9461eeace"
                :type shuttle_subject_mapping_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_subject_mappings/',
                        to_string(shuttle_subject_mapping_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def get_shuttle_discovered_subjects_v2026_r0(
        self,
        job_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleDiscoveredSubjectsV2026R0:
        """
                Returns a paginated list of subjects discovered on the source system for

                the shuttle job identified by `job_id`.

                :param job_id: The unique identifier of the shuttle job whose discovered subjects to list.
                :type job_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'job_id': to_string(job_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_discovered_subjects',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleDiscoveredSubjectsV2026R0)

    def get_shuttle_path_entries_v2026_r0(
        self,
        job_id: str,
        side: GetShuttlePathEntriesV2026R0Side,
        *,
        path: Optional[str] = None,
        path_id: Optional[str] = None,
        account_email: Optional[str] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttlePathEntriesV2026R0:
        """
                Returns a paginated list of source or target path entries for a shuttle

                job. Call with only `job_id` and `side` to list the roots, then browse one


                level at a time using `path`, `path_id`, or both. Each entry includes


                `path`, `path_id`, `is_directory`, and a `scope` object (`account` or


                `shared_space`) so a mapping can be created from that row without extra


                browse state. Valid values depend on the selected system.

                :param job_id: The unique identifier of the shuttle job whose path entries to list.
                :type job_id: str
                :param side: The side of the migration to browse.
                :type side: GetShuttlePathEntriesV2026R0Side
                :param path: The human-readable parent path whose children are returned. This can
        be used with or without `path_id`. Omit both, or pass `/` as `path`,
        to list root entries., defaults to None
                :type path: Optional[str], optional
                :param path_id: The `path_id` value of the parent entry whose children are
        returned. This can be used with or without `path`. It distinguishes
        paths with identical names on systems that support stable identifiers., defaults to None
                :type path_id: Optional[str], optional
                :param account_email: The email of the account whose path entries are returned. This is a
        system-native identifier and is not always an RFC 5322 address., defaults to None
                :type account_email: Optional[str], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'job_id': to_string(job_id),
                'side': to_string(side),
                'path': to_string(path),
                'path_id': to_string(path_id),
                'account_email': to_string(account_email),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_path_entries',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttlePathEntriesV2026R0)

    def get_shuttle_mapping_errors_v2026_r0(
        self,
        job_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleMappingErrorsV2026R0:
        """
                Returns a paginated list of mapping errors for a shuttle job. Only the latest

                record for each error is returned. The revision field identifies the mapping


                revision in which that error was generated.

                :param job_id: The unique identifier of the shuttle job whose mapping errors to list.
                :type job_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'job_id': to_string(job_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_mapping_errors',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleMappingErrorsV2026R0)

    def get_shuttle_reports_v2026_r0(
        self,
        run_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleReportsV2026R0:
        """
                Returns a paginated list of reports generated for the shuttle run

                identified by `run_id`.

                :param run_id: The unique identifier of the shuttle run whose reports to list.
                :type run_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'run_id': to_string(run_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shuttle_reports']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleReportsV2026R0)

    def create_shuttle_report_v2026_r0(
        self,
        run_id: str,
        format: CreateShuttleReportV2026R0Format,
        sections: List[str],
        *,
        users_scope: Optional[CreateShuttleReportV2026R0UsersScope] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleReportV2026R0:
        """
                Requests asynchronous generation of a report for a shuttle run. The

                report is returned immediately in `pending` or `processing` status.


                Poll `GET /shuttle_reports/{shuttle_report_id}` while `status` is


                `pending` or `processing`. Stop when `status` is `complete`, `failed`,


                `canceled`, or `unknown`. Repeating this request with the same


                parameters reuses the existing report instead of creating a duplicate.

                :param run_id: The unique identifier of the shuttle run to generate a report for.
                :type run_id: str
                :param format: The output file format of the report.
                :type format: CreateShuttleReportV2026R0Format
                :param sections: The sections to include in the report. Must be a non-empty subset of
        the run's `available_report_sections`. This is an open list whose set
        of values is expected to grow; the currently documented values include
        `files_and_folders`, `event_log`, `transfer_overview`, `source_users`,
        `target_users`, `source_collaborators`, `target_collaborators`,
        `source_collaborations`, and `target_collaborations`.
                :type sections: List[str]
                :param users_scope: Which users to include in user-related report sections. Defaults to
        `migrated` when omitted., defaults to None
                :type users_scope: Optional[CreateShuttleReportV2026R0UsersScope], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'run_id': run_id,
            'format': format,
            'sections': sections,
            'users_scope': users_scope,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shuttle_reports']
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleReportV2026R0)

    def get_shuttle_report_by_id_v2026_r0(
        self,
        shuttle_report_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShuttleReportV2026R0:
        """
                Returns details for a single shuttle report identified by its ID,

                including generation status and, once generation finishes, the Box


                output reference.

                :param shuttle_report_id: The unique identifier for the shuttle report.
        Example: "6a3ba8d14f2c91e8370b4d12"
                :type shuttle_report_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shuttle_reports/',
                        to_string(shuttle_report_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShuttleReportV2026R0)
