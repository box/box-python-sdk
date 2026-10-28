from typing import Union

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_input_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationInputV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

ShuttlePathMappingLocationInputV2026R0 = Union[
    ShuttlePathMappingAccountLocationInputV2026R0,
    ShuttlePathMappingSharedSpaceLocationInputV2026R0,
]
