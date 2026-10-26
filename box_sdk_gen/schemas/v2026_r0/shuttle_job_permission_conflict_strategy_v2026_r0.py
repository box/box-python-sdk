from enum import Enum

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleJobPermissionConflictStrategyV2026R0(str, Enum):
    PRESERVE_STRUCTURE_RESTRICT_SHARING = 'preserve_structure_restrict_sharing'
    PRESERVE_STRUCTURE_EXPAND_SHARING = 'preserve_structure_expand_sharing'
    PRESERVE_SHARING_MODIFY_STRUCTURE = 'preserve_sharing_modify_structure'
    WARN_PERMISSIONS_CONFLICTS = 'warn_permissions_conflicts'
