from typing import Optional

from box_sdk_gen.schemas.user_base import UserBaseTypeField

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError


class UserCollaborations(UserBase):
    def __init__(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        login: Optional[str] = None,
        is_active: Optional[bool] = None,
        type: UserBaseTypeField = UserBaseTypeField.USER,
        **kwargs
    ):
        """
        :param id: The unique identifier for this user.
        :type id: str
        :param name: The display name of this user. If the collaboration status is `pending`, an empty string is returned., defaults to None
        :type name: Optional[str], optional
        :param login: The primary email address of this user. If the collaboration status is `pending`, an empty string is returned., defaults to None
        :type login: Optional[str], optional
        :param is_active: If set to `false`, the user is either deactivated or deleted., defaults to None
        :type is_active: Optional[bool], optional
        :param type: The value will always be `user`., defaults to UserBaseTypeField.USER
        :type type: UserBaseTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.name = name
        self.login = login
        self.is_active = is_active
