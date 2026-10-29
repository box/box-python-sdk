from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_input_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_target_input_v2026_r0 import (
    ShuttlePathMappingAccountLocationTargetInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_target_input_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationTargetInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_location_input_v2026_r0 import (
    ShuttlePathMappingLocationInputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_target_location_input_v2026_r0 import (
    ShuttlePathMappingTargetLocationInputV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingUpdateRequestV2026R0(BaseObject):
    def __init__(
        self,
        *,
        is_path_skipped: Optional[bool] = None,
        source: Optional[ShuttlePathMappingLocationInputV2026R0] = None,
        target: Optional[ShuttlePathMappingTargetLocationInputV2026R0] = None,
        **kwargs
    ):
        """
                :param is_path_skipped: Whether this source path should be skipped during the migration., defaults to None
                :type is_path_skipped: Optional[bool], optional
                :param target: The destination location to migrate to. Set to `null` to clear the
        destination, for example when skipping the source path., defaults to None
                :type target: Optional[ShuttlePathMappingTargetLocationInputV2026R0], optional
        """
        super().__init__(**kwargs)
        self.is_path_skipped = is_path_skipped
        self.source = source
        self.target = target
