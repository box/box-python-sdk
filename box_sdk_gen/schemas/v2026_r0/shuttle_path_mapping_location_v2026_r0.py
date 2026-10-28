from typing import Union

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_v2026_r0 import (
    ShuttlePathMappingAccountLocationV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

ShuttlePathMappingLocationV2026R0 = Union[
    ShuttlePathMappingAccountLocationV2026R0,
    ShuttlePathMappingSharedSpaceLocationV2026R0,
]
