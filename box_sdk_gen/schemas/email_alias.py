from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class EmailAliasTypeField(str, Enum):
    EMAIL_ALIAS = 'email_alias'


class EmailAlias(BaseObject):
    _discriminator = 'type', {'email_alias'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[EmailAliasTypeField] = None,
        email: Optional[str] = None,
        is_confirmed: Optional[bool] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this object., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `email_alias`., defaults to None
        :type type: Optional[EmailAliasTypeField], optional
        :param email: The email address., defaults to None
        :type email: Optional[str], optional
        :param is_confirmed: Whether the email address has been confirmed., defaults to None
        :type is_confirmed: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.email = email
        self.is_confirmed = is_confirmed
