from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_path_entry_account_scope_v2026_r0 import (
    ShuttlePathEntryAccountScopeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_entry_shared_space_scope_v2026_r0 import (
    ShuttlePathEntrySharedSpaceScopeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_entry_scope_v2026_r0 import (
    ShuttlePathEntryScopeV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathEntryV2026R0TypeField(str, Enum):
    SHUTTLE_PATH_ENTRY = 'shuttle_path_entry'


class ShuttlePathEntryV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_path_entry'}

    def __init__(
        self,
        id: str,
        name: str,
        path: str,
        scope: ShuttlePathEntryScopeV2026R0,
        is_directory: bool,
        can_map: bool,
        *,
        type: ShuttlePathEntryV2026R0TypeField = ShuttlePathEntryV2026R0TypeField.SHUTTLE_PATH_ENTRY,
        path_id: Optional[str] = None,
        parent_path: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier of this browse row. This is not the account
        identifier; when `scope.type` is `account`, the account identifier is
        `scope.id`.
                :type id: str
                :param name: The display name of the path entry.
                :type name: str
                :param path: The human-readable path of the entry.
                :type path: str
                :param is_directory: Whether the entry is a directory (`true`) or a single file
        (`false`). Maps to `is_directory` on a path mapping location.
                :type is_directory: bool
                :param can_map: Whether the entry can be selected in a path mapping.
                :type can_map: bool
                :param type: The value will always be `shuttle_path_entry`., defaults to ShuttlePathEntryV2026R0TypeField.SHUTTLE_PATH_ENTRY
                :type type: ShuttlePathEntryV2026R0TypeField, optional
                :param path_id: The system-native identifier of the path. `null` when the selected
        system does not provide one. Maps to `path_id` on a path mapping
        location., defaults to None
                :type path_id: Optional[str], optional
                :param parent_path: The human-readable path of the parent entry, or `null` for a root
        entry., defaults to None
                :type parent_path: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.path = path
        self.scope = scope
        self.is_directory = is_directory
        self.can_map = can_map
        self.type = type
        self.path_id = path_id
        self.parent_path = parent_path
