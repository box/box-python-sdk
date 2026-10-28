from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_v2026_r0 import ShuttleSubjectV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_target_subject_v2026_r0 import (
    ShuttleTargetSubjectV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSubjectMappingV2026R0TypeField(str, Enum):
    SHUTTLE_SUBJECT_MAPPING = 'shuttle_subject_mapping'


class ShuttleSubjectMappingV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_subject_mapping'}

    def __init__(
        self,
        id: str,
        job_id: str,
        is_subject_skipped: bool,
        source: ShuttleSubjectV2026R0,
        *,
        type: ShuttleSubjectMappingV2026R0TypeField = ShuttleSubjectMappingV2026R0TypeField.SHUTTLE_SUBJECT_MAPPING,
        discovered_subject_id: Optional[str] = None,
        revision: Optional[int] = None,
        target: Optional[ShuttleTargetSubjectV2026R0] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shuttle subject mapping.
                :type id: str
                :param job_id: The unique identifier of the shuttle job this mapping belongs to.
                :type job_id: str
                :param is_subject_skipped: Whether this subject is skipped during the migration.
                :type is_subject_skipped: bool
                :param type: The value will always be `shuttle_subject_mapping`., defaults to ShuttleSubjectMappingV2026R0TypeField.SHUTTLE_SUBJECT_MAPPING
                :type type: ShuttleSubjectMappingV2026R0TypeField, optional
                :param discovered_subject_id: The unique identifier of the discovered subject this mapping applies to.
        `null` for legacy mappings created before this field was tracked., defaults to None
                :type discovered_subject_id: Optional[str], optional
                :param revision: The discovery-requirements revision this mapping was resolved against.
        `null` for legacy mappings., defaults to None
                :type revision: Optional[int], optional
                :param target: The Box target subject. `null` when the subject is skipped or not yet
        assigned., defaults to None
                :type target: Optional[ShuttleTargetSubjectV2026R0], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.job_id = job_id
        self.is_subject_skipped = is_subject_skipped
        self.source = source
        self.type = type
        self.discovered_subject_id = discovered_subject_id
        self.revision = revision
        self.target = target
