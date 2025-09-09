from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class CollaborationAllowlistExemptTargetTypeField(str, Enum):
    COLLABORATION_WHITELIST_EXEMPT_TARGET = 'collaboration_whitelist_exempt_target'


class CollaborationAllowlistExemptTargetEnterpriseTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class CollaborationAllowlistExemptTargetEnterpriseField(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CollaborationAllowlistExemptTargetEnterpriseTypeField] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[CollaborationAllowlistExemptTargetEnterpriseTypeField], optional
        :param name: The name of the enterprise., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name


class CollaborationAllowlistExemptTarget(BaseObject):
    _discriminator = 'type', {'collaboration_whitelist_exempt_target'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CollaborationAllowlistExemptTargetTypeField] = None,
        enterprise: Optional[CollaborationAllowlistExemptTargetEnterpriseField] = None,
        user: Optional[UserMini] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this exemption., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `collaboration_whitelist_exempt_target`., defaults to None
        :type type: Optional[CollaborationAllowlistExemptTargetTypeField], optional
        :param created_at: The time the entry was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: The time the entry was modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.enterprise = enterprise
        self.user = user
        self.created_at = created_at
        self.modified_at = modified_at
