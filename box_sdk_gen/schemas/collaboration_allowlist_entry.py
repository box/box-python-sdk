from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class CollaborationAllowlistEntryTypeField(str, Enum):
    COLLABORATION_WHITELIST_ENTRY = 'collaboration_whitelist_entry'


class CollaborationAllowlistEntryDirectionField(str, Enum):
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'
    BOTH = 'both'


class CollaborationAllowlistEntryEnterpriseTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class CollaborationAllowlistEntryEnterpriseField(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CollaborationAllowlistEntryEnterpriseTypeField] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[CollaborationAllowlistEntryEnterpriseTypeField], optional
        :param name: The name of the enterprise., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name


class CollaborationAllowlistEntry(BaseObject):
    _discriminator = 'type', {'collaboration_whitelist_entry'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CollaborationAllowlistEntryTypeField] = None,
        domain: Optional[str] = None,
        direction: Optional[CollaborationAllowlistEntryDirectionField] = None,
        enterprise: Optional[CollaborationAllowlistEntryEnterpriseField] = None,
        created_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this entry., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `collaboration_whitelist_entry`., defaults to None
        :type type: Optional[CollaborationAllowlistEntryTypeField], optional
        :param domain: The whitelisted domain., defaults to None
        :type domain: Optional[str], optional
        :param direction: The direction of the collaborations to allow., defaults to None
        :type direction: Optional[CollaborationAllowlistEntryDirectionField], optional
        :param created_at: The time the entry was created at., defaults to None
        :type created_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.domain = domain
        self.direction = direction
        self.enterprise = enterprise
        self.created_at = created_at
