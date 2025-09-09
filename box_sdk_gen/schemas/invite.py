from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class InviteTypeField(str, Enum):
    INVITE = 'invite'


class InviteInvitedToTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class InviteInvitedToField(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[InviteInvitedToTypeField] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[InviteInvitedToTypeField], optional
        :param name: The name of the enterprise., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name


class Invite(BaseObject):
    _discriminator = 'type', {'invite'}

    def __init__(
        self,
        id: str,
        *,
        type: InviteTypeField = InviteTypeField.INVITE,
        invited_to: Optional[InviteInvitedToField] = None,
        actionable_by: Optional[UserMini] = None,
        invited_by: Optional[UserMini] = None,
        status: Optional[str] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this invite.
        :type id: str
        :param type: The value will always be `invite`., defaults to InviteTypeField.INVITE
        :type type: InviteTypeField, optional
        :param invited_to: A representation of a Box enterprise., defaults to None
        :type invited_to: Optional[InviteInvitedToField], optional
        :param status: The status of the invite., defaults to None
        :type status: Optional[str], optional
        :param created_at: When the invite was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: When the invite was modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.invited_to = invited_to
        self.actionable_by = actionable_by
        self.invited_by = invited_by
        self.status = status
        self.created_at = created_at
        self.modified_at = modified_at
