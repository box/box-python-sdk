from typing import Union

from box_sdk_gen.schemas.v2026_r0.shuttle_path_entry_account_scope_v2026_r0 import (
    ShuttlePathEntryAccountScopeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_entry_shared_space_scope_v2026_r0 import (
    ShuttlePathEntrySharedSpaceScopeV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

ShuttlePathEntryScopeV2026R0 = Union[
    ShuttlePathEntryAccountScopeV2026R0, ShuttlePathEntrySharedSpaceScopeV2026R0
]
