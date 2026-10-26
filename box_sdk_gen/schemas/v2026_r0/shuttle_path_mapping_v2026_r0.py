from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_location_v2026_r0 import (
    ShuttlePathMappingAccountLocationV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_shared_space_location_v2026_r0 import (
    ShuttlePathMappingSharedSpaceLocationV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_location_v2026_r0 import (
    ShuttlePathMappingLocationV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingV2026R0TypeField(str, Enum):
    SHUTTLE_PATH_MAPPING = 'shuttle_path_mapping'


class ShuttlePathMappingV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_path_mapping'}

    def __init__(
        self,
        id: str,
        job_id: str,
        is_path_skipped: bool,
        source: ShuttlePathMappingLocationV2026R0,
        *,
        type: ShuttlePathMappingV2026R0TypeField = ShuttlePathMappingV2026R0TypeField.SHUTTLE_PATH_MAPPING,
        target: Optional[ShuttlePathMappingLocationV2026R0] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shuttle path mapping.
                :type id: str
                :param job_id: The unique identifier of the shuttle job this mapping belongs to.
                :type job_id: str
                :param is_path_skipped: Whether this source path is skipped during the migration.
                :type is_path_skipped: bool
                :param type: The value will always be `shuttle_path_mapping`., defaults to ShuttlePathMappingV2026R0TypeField.SHUTTLE_PATH_MAPPING
                :type type: ShuttlePathMappingV2026R0TypeField, optional
                :param target: The destination location. `null` when the source path is skipped or
        the job has no destination, such as an analysis job., defaults to None
                :type target: Optional[ShuttlePathMappingLocationV2026R0], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.job_id = job_id
        self.is_path_skipped = is_path_skipped
        self.source = source
        self.type = type
        self.target = target
