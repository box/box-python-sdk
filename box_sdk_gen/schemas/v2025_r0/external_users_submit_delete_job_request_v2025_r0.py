from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.user_reference_v2025_r0 import UserReferenceV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class ExternalUsersSubmitDeleteJobRequestV2025R0(BaseObject):
    def __init__(self, external_users: List[UserReferenceV2025R0], **kwargs):
        """
        :param external_users: List of external users to delete.
        :type external_users: List[UserReferenceV2025R0]
        """
        super().__init__(**kwargs)
        self.external_users = external_users
