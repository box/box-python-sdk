from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_target_subject_input_v2026_r0 import (
    ShuttleTargetSubjectInputV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSubjectMappingCreateRequestV2026R0(BaseObject):
    def __init__(
        self,
        job_id: str,
        discovered_subject_id: str,
        *,
        revision: Optional[int] = None,
        is_subject_skipped: Optional[bool] = None,
        target: Optional[ShuttleTargetSubjectInputV2026R0] = None,
        **kwargs
    ):
        """
                :param job_id: The unique identifier of the shuttle job this mapping belongs to.
                :type job_id: str
                :param discovered_subject_id: The unique identifier of the discovered subject to map.
                :type discovered_subject_id: str
                :param revision: The discovery-requirements revision to resolve against. Omit to use the
        latest revision., defaults to None
                :type revision: Optional[int], optional
                :param is_subject_skipped: Whether this subject should be skipped during the migration. Defaults
        to `false`., defaults to None
                :type is_subject_skipped: Optional[bool], optional
                :param target: The Box target to map to. Omit or set to `null` when the subject is
        skipped., defaults to None
                :type target: Optional[ShuttleTargetSubjectInputV2026R0], optional
        """
        super().__init__(**kwargs)
        self.job_id = job_id
        self.discovered_subject_id = discovered_subject_id
        self.revision = revision
        self.is_subject_skipped = is_subject_skipped
        self.target = target
