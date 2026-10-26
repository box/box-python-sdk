from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_v2026_r0 import ShuttleSubjectV2026R0

from box_sdk_gen.schemas.v2026_r0.shuttle_target_subject_v2026_r0 import (
    ShuttleTargetSubjectV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleDiscoveredSubjectV2026R0TypeField(str, Enum):
    SHUTTLE_DISCOVERED_SUBJECT = 'shuttle_discovered_subject'


class ShuttleDiscoveredSubjectV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_discovered_subject'}

    def __init__(
        self,
        id: str,
        job_id: str,
        revision: int,
        source: ShuttleSubjectV2026R0,
        *,
        type: ShuttleDiscoveredSubjectV2026R0TypeField = ShuttleDiscoveredSubjectV2026R0TypeField.SHUTTLE_DISCOVERED_SUBJECT,
        suggested_target: Optional[ShuttleTargetSubjectV2026R0] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the discovered subject.
                :type id: str
                :param job_id: The unique identifier of the shuttle job this subject belongs to.
                :type job_id: str
                :param revision: The scan revision this discovered subject belongs to.
                :type revision: int
                :param type: The value will always be `shuttle_discovered_subject`., defaults to ShuttleDiscoveredSubjectV2026R0TypeField.SHUTTLE_DISCOVERED_SUBJECT
                :type type: ShuttleDiscoveredSubjectV2026R0TypeField, optional
                :param suggested_target: A suggested Box target inferred during the scan. `null` when no
        suggestion was made., defaults to None
                :type suggested_target: Optional[ShuttleTargetSubjectV2026R0], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.job_id = job_id
        self.revision = revision
        self.source = source
        self.type = type
        self.suggested_target = suggested_target
