from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.v2026_r0.shuttle_job_permission_conflict_strategy_v2026_r0 import (
    ShuttleJobPermissionConflictStrategyV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleJobUpdateRequestV2026R0AccountMappingField(BaseObject):
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


class ShuttleJobUpdateRequestV2026R0SettingsField(BaseObject):
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


class ShuttleJobUpdateRequestV2026R0(BaseObject):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        account_mapping: Optional[
            ShuttleJobUpdateRequestV2026R0AccountMappingField
        ] = None,
        settings: Optional[ShuttleJobUpdateRequestV2026R0SettingsField] = None,
        **kwargs
    ):
        """
                :param name: The human-readable name of the shuttle job., defaults to None
                :type name: Optional[str], optional
                :param comment: An optional free-form comment describing the shuttle job., defaults to None
                :type comment: Optional[str], optional
                :param tags: A list of free-form tags associated with the shuttle job., defaults to None
                :type tags: Optional[List[str]], optional
                :param account_mapping: The account mapping configuration that controls how source identities
        and permissions are translated into Box., defaults to None
                :type account_mapping: Optional[ShuttleJobUpdateRequestV2026R0AccountMappingField], optional
                :param settings: The tunable settings that control how the shuttle job runs., defaults to None
                :type settings: Optional[ShuttleJobUpdateRequestV2026R0SettingsField], optional
        """
        super().__init__(**kwargs)
        self.name = name
        self.comment = comment
        self.tags = tags
        self.account_mapping = account_mapping
        self.settings = settings
