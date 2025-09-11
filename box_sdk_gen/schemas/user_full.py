from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.user_base import UserBaseTypeField

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.user import UserStatusField

from box_sdk_gen.schemas.user import UserNotificationEmailField

from box_sdk_gen.schemas.user import User

from box_sdk_gen.schemas.tracking_code import TrackingCode

from box_sdk_gen.box.errors import BoxSDKError


class UserFullRoleField(str, Enum):
    ADMIN = 'admin'
    COADMIN = 'coadmin'
    USER = 'user'


class UserFullEnterpriseTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class UserFullEnterpriseField(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[UserFullEnterpriseTypeField] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[UserFullEnterpriseTypeField], optional
        :param name: The name of the enterprise., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name


class UserFull(User):
    def __init__(
        self,
        id: str,
        *,
        role: Optional[UserFullRoleField] = None,
        tracking_codes: Optional[List[TrackingCode]] = None,
        can_see_managed_users: Optional[bool] = None,
        is_sync_enabled: Optional[bool] = None,
        is_external_collab_restricted: Optional[bool] = None,
        is_exempt_from_device_limits: Optional[bool] = None,
        is_exempt_from_login_verification: Optional[bool] = None,
        enterprise: Optional[UserFullEnterpriseField] = None,
        my_tags: Optional[List[str]] = None,
        hostname: Optional[str] = None,
        is_platform_access_only: Optional[bool] = None,
        external_app_user_id: Optional[str] = None,
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
                :param role: The user’s enterprise role., defaults to None
                :type role: Optional[UserFullRoleField], optional
                :param tracking_codes: Tracking codes allow an admin to generate reports from the
        admin console and assign an attribute to a specific group
        of users. This setting must be enabled for an enterprise
        before it can be used., defaults to None
                :type tracking_codes: Optional[List[TrackingCode]], optional
                :param can_see_managed_users: Whether the user can see other enterprise users in their contact list., defaults to None
                :type can_see_managed_users: Optional[bool], optional
                :param is_sync_enabled: Whether the user can use Box Sync., defaults to None
                :type is_sync_enabled: Optional[bool], optional
                :param is_external_collab_restricted: Whether the user is allowed to collaborate with users outside their
        enterprise., defaults to None
                :type is_external_collab_restricted: Optional[bool], optional
                :param is_exempt_from_device_limits: Whether to exempt the user from Enterprise device limits., defaults to None
                :type is_exempt_from_device_limits: Optional[bool], optional
                :param is_exempt_from_login_verification: Whether the user must use two-factor authentication., defaults to None
                :type is_exempt_from_login_verification: Optional[bool], optional
                :param my_tags: Tags for all files and folders owned by the user. Values returned
        will only contain tags that were set by the requester., defaults to None
                :type my_tags: Optional[List[str]], optional
                :param hostname: The root (protocol, subdomain, domain) of any links that need to be
        generated for the user., defaults to None
                :type hostname: Optional[str], optional
                :param is_platform_access_only: Whether the user is an App User., defaults to None
                :type is_platform_access_only: Optional[bool], optional
                :param external_app_user_id: An external identifier for an app user, which can be used to look up
        the user. This can be used to tie user IDs from external identity
        providers to Box users., defaults to None
                :type external_app_user_id: Optional[str], optional
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
        super().__init__(
            id=id,
            created_at=created_at,
            modified_at=modified_at,
            language=language,
            timezone=timezone,
            space_amount=space_amount,
            space_used=space_used,
            max_upload_size=max_upload_size,
            status=status,
            job_title=job_title,
            phone=phone,
            address=address,
            avatar_url=avatar_url,
            notification_email=notification_email,
            name=name,
            login=login,
            type=type,
            **kwargs
        )
        self.role = role
        self.tracking_codes = tracking_codes
        self.can_see_managed_users = can_see_managed_users
        self.is_sync_enabled = is_sync_enabled
        self.is_external_collab_restricted = is_external_collab_restricted
        self.is_exempt_from_device_limits = is_exempt_from_device_limits
        self.is_exempt_from_login_verification = is_exempt_from_login_verification
        self.enterprise = enterprise
        self.my_tags = my_tags
        self.hostname = hostname
        self.is_platform_access_only = is_platform_access_only
        self.external_app_user_id = external_app_user_id
