from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import List

from box_sdk_gen.schemas.v2026_r0.shuttle_job_permission_conflict_strategy_v2026_r0 import (
    ShuttleJobPermissionConflictStrategyV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleJobV2026R0TypeField(str, Enum):
    SHUTTLE_JOB = 'shuttle_job'


class ShuttleJobV2026R0JobTypeField(str, Enum):
    TRANSFER = 'transfer'
    ANALYSIS = 'analysis'


class ShuttleJobV2026R0SourceSystemTypeField(str, Enum):
    SHUTTLE_SYSTEM = 'shuttle_system'


class ShuttleJobV2026R0SourceSystemField(BaseObject):
    _discriminator = 'type', {'shuttle_system'}

    def __init__(
        self,
        id: str,
        name: str,
        *,
        type: ShuttleJobV2026R0SourceSystemTypeField = ShuttleJobV2026R0SourceSystemTypeField.SHUTTLE_SYSTEM,
        **kwargs
    ):
        """
        :param id: The unique identifier for the source system.
        :type id: str
        :param name: The human-readable name of the source system.
        :type name: str
        :param type: The value will always be `shuttle_system`., defaults to ShuttleJobV2026R0SourceSystemTypeField.SHUTTLE_SYSTEM
        :type type: ShuttleJobV2026R0SourceSystemTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.type = type


class ShuttleJobV2026R0AccountMappingField(BaseObject):
    def __init__(
        self,
        is_enabled: bool,
        *,
        permission_conflict_strategy: Optional[
            ShuttleJobPermissionConflictStrategyV2026R0
        ] = None,
        are_external_shares_mapped: Optional[bool] = None,
        are_permissions_mapped: Optional[bool] = None,
        **kwargs
    ):
        """
                :param is_enabled: Whether account mapping is enabled for the shuttle job.
                :type is_enabled: bool
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


class ShuttleJobV2026R0SettingsField(BaseObject):
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


class ShuttleJobV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_job'}

    def __init__(
        self,
        id: str,
        name: str,
        job_type: ShuttleJobV2026R0JobTypeField,
        state: str,
        mapping_state: str,
        source_system: ShuttleJobV2026R0SourceSystemField,
        *,
        type: ShuttleJobV2026R0TypeField = ShuttleJobV2026R0TypeField.SHUTTLE_JOB,
        comment: Optional[str] = None,
        account_mapping: Optional[ShuttleJobV2026R0AccountMappingField] = None,
        tags: Optional[List[str]] = None,
        settings: Optional[ShuttleJobV2026R0SettingsField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shuttle job.
                :type id: str
                :param name: The human-readable name of the shuttle job.
                :type name: str
                :param job_type: The type of work the shuttle job performs.
                :type job_type: ShuttleJobV2026R0JobTypeField
                :param state: The current state of the shuttle job. This is an open string whose set
        of values is expected to grow; the currently documented values include
        `created`, `started`, `stopped`, `completed`, `failed`, `invalid`, and
        `unknown`. Clients should treat any value they do not recognize as
        `unknown`.
                :type state: str
                :param mapping_state: The current mapping-preparation state of the job. This is an open string
        whose set of values is expected to grow; the currently documented values
        include `awaiting_path_mapping`, `importing_paths`,
        `paths_import_rejected`, `paths_invalid`, `paths_ready`,
        `scanning_source`, `source_scan_failed`, `source_scan_out_of_date`,
        `awaiting_subject_mapping`, `importing_subjects`,
        `subjects_import_rejected`, `mapping_complete`, `building_map`,
        `map_build_failed`, `map_out_of_date`, and `ready`.
        `paths_import_rejected` means the last path-mapping spreadsheet was
        rejected or failed and the path mappings have not been changed since;
        it clears on the next import or the next manual path-mapping change.
        `subjects_import_rejected` means the last subject-mapping spreadsheet
        was rejected or failed and the subject mappings have not been changed
        since; it clears on the next import or the next manual subject-mapping
        change.
                :type mapping_state: str
                :param source_system: The source system the shuttle job migrates content from.
                :type source_system: ShuttleJobV2026R0SourceSystemField
                :param type: The value will always be `shuttle_job`., defaults to ShuttleJobV2026R0TypeField.SHUTTLE_JOB
                :type type: ShuttleJobV2026R0TypeField, optional
                :param comment: An optional free-form comment describing the shuttle job., defaults to None
                :type comment: Optional[str], optional
                :param account_mapping: The account mapping configuration that controls how source identities
        and permissions are translated into Box., defaults to None
                :type account_mapping: Optional[ShuttleJobV2026R0AccountMappingField], optional
                :param tags: A list of free-form tags associated with the shuttle job., defaults to None
                :type tags: Optional[List[str]], optional
                :param settings: The tunable settings that control how the shuttle job runs., defaults to None
                :type settings: Optional[ShuttleJobV2026R0SettingsField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.job_type = job_type
        self.state = state
        self.mapping_state = mapping_state
        self.source_system = source_system
        self.type = type
        self.comment = comment
        self.account_mapping = account_mapping
        self.tags = tags
        self.settings = settings
