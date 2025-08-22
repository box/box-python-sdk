from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ExternalUserDeletionResultV2025R0(BaseObject):
    def __init__(
        self, user_id: str, status: int, *, detail: Optional[str] = None, **kwargs
    ):
        """
        :param user_id: The ID of the external user.
        :type user_id: str
        :param status: HTTP status code for a specific user's deletion request.
        :type status: int
        :param detail: Deletion request status details. This property is only present when the deletion request is not successful., defaults to None
        :type detail: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.user_id = user_id
        self.status = status
        self.detail = detail
