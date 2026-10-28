from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_target_subject_input_v2026_r0 import (
    ShuttleTargetSubjectInputV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSubjectMappingUpdateRequestV2026R0(BaseObject):
    def __init__(
        self,
        *,
        is_subject_skipped: Optional[bool] = None,
        target: Optional[ShuttleTargetSubjectInputV2026R0] = None,
        **kwargs
    ):
        """
                :param is_subject_skipped: Whether this subject should be skipped during the migration., defaults to None
                :type is_subject_skipped: Optional[bool], optional
                :param target: The Box target to map to. Set to `null` only for a skipped subject.
        Setting it to `null` while the mapping is active fails validation.
        Updating `is_subject_skipped` alone preserves the existing target., defaults to None
                :type target: Optional[ShuttleTargetSubjectInputV2026R0], optional
        """
        super().__init__(**kwargs)
        self.is_subject_skipped = is_subject_skipped
        self.target = target
