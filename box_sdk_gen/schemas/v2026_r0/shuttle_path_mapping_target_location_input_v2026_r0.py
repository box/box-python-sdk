from typing import Union

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_target_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationTargetInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_target_input_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationTargetInputV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

ShuttlePathMappingTargetLocationInputV2026R0 = Union[
    ShuttlePathMappingAccountLocationTargetInputV2026R0,
    ShuttlePathMappingSharedSpaceLocationTargetInputV2026R0,
]
