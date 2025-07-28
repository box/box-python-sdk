from typing import Optional

from box_sdk_gen.schemas.v2025_r0.user_base_v2025_r0 import UserBaseV2025R0TypeField

from box_sdk_gen.schemas.v2025_r0.user_base_v2025_r0 import UserBaseV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class HubCollaborationUserV2025R0(UserBaseV2025R0):
    def __init__(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        login: Optional[str] = None,
        type: UserBaseV2025R0TypeField = UserBaseV2025R0TypeField.USER,
        **kwargs
    ):
        """
        :param id: The unique identifier for this user.
        :type id: str
        :param name: The display name of this user. If the collaboration status is `pending`, an empty string is returned., defaults to None
        :type name: Optional[str], optional
        :param login: The primary email address of this user. If the collaboration status is `pending`, an empty string is returned., defaults to None
        :type login: Optional[str], optional
        :param type: The value will always be `user`., defaults to UserBaseV2025R0TypeField.USER
        :type type: UserBaseV2025R0TypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.name = name
        self.login = login
