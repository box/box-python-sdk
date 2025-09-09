from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_base import UserBaseTypeField

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class UserStatusField(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    CANNOT_DELETE_EDIT = 'cannot_delete_edit'
    CANNOT_DELETE_EDIT_UPLOAD = 'cannot_delete_edit_upload'


class UserNotificationEmailField(BaseObject):
    def __init__(
        self,
        *,
        email: Optional[str] = None,
        is_confirmed: Optional[bool] = None,
        **kwargs
    ):
        """
        :param email: The email address to send the notifications to., defaults to None
        :type email: Optional[str], optional
        :param is_confirmed: Specifies if this email address has been confirmed., defaults to None
        :type is_confirmed: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.email = email
        self.is_confirmed = is_confirmed


class User(UserMini):
    def __init__(
        self,
        id: str,
        *,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        language: Optional[str] = None,
        timezone: Optional[str] = None,
        space_amount: Optional[int] = None,
        space_used: Optional[int] = None,
        max_upload_size: Optional[int] = None,
        status: Optional[UserStatusField] = None,
        job_title: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        avatar_url: Optional[str] = None,
        notification_email: Optional[UserNotificationEmailField] = None,
        name: Optional[str] = None,
        login: Optional[str] = None,
        type: UserBaseTypeField = UserBaseTypeField.USER,
        **kwargs
    ):
        """
                :param id: The unique identifier for this user.
                :type id: str
                :param created_at: When the user object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When the user object was last modified., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param language: The language of the user, formatted in modified version of the
        [ISO 639-1](/guides/api-calls/language-codes) format., defaults to None
                :type language: Optional[str], optional
                :param timezone: The user's timezone., defaults to None
                :type timezone: Optional[str], optional
                :param space_amount: The user’s total available space amount in bytes., defaults to None
                :type space_amount: Optional[int], optional
                :param space_used: The amount of space in use by the user., defaults to None
                :type space_used: Optional[int], optional
                :param max_upload_size: The maximum individual file size in bytes the user can have., defaults to None
                :type max_upload_size: Optional[int], optional
                :param status: The user's account status., defaults to None
                :type status: Optional[UserStatusField], optional
                :param job_title: The user’s job title., defaults to None
                :type job_title: Optional[str], optional
                :param phone: The user’s phone number., defaults to None
                :type phone: Optional[str], optional
                :param address: The user’s address., defaults to None
                :type address: Optional[str], optional
                :param avatar_url: URL of the user’s avatar image., defaults to None
                :type avatar_url: Optional[str], optional
                :param notification_email: An alternate notification email address to which email
        notifications are sent. When it's confirmed, this will be
        the email address to which notifications are sent instead of
        to the primary email address., defaults to None
                :type notification_email: Optional[UserNotificationEmailField], optional
                :param name: The display name of this user., defaults to None
                :type name: Optional[str], optional
                :param login: The primary email address of this user., defaults to None
                :type login: Optional[str], optional
                :param type: The value will always be `user`., defaults to UserBaseTypeField.USER
                :type type: UserBaseTypeField, optional
        """
        super().__init__(id=id, name=name, login=login, type=type, **kwargs)
        self.created_at = created_at
        self.modified_at = modified_at
        self.language = language
        self.timezone = timezone
        self.space_amount = space_amount
        self.space_used = space_used
        self.max_upload_size = max_upload_size
        self.status = status
        self.job_title = job_title
        self.phone = phone
        self.address = address
        self.avatar_url = avatar_url
        self.notification_email = notification_email
