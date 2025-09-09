from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.external_user_deletion_result_v2025_r0 import (
    ExternalUserDeletionResultV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ExternalUsersSubmitDeleteJobResponseV2025R0(BaseObject):
    def __init__(self, entries: List[ExternalUserDeletionResultV2025R0], **kwargs):
        """
        :param entries: Array of results of each external user deletion request.
        :type entries: List[ExternalUserDeletionResultV2025R0]
        """
        super().__init__(**kwargs)
        self.entries = entries
