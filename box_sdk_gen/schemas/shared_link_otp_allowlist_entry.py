from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class SharedLinkOtpAllowlistEntryTypeField(str, Enum):
    EMAIL = 'email'
    DOMAIN = 'domain'


class SharedLinkOtpAllowlistEntry(BaseObject):
    _discriminator = 'type', {'email', 'domain'}

    def __init__(
        self,
        type: SharedLinkOtpAllowlistEntryTypeField,
        value: str,
        created_at: DateTime,
        created_by: UserBase,
        **kwargs
    ):
        """
                :param type: The kind of allowlist entry.

        * `email` - The entry matches a single email address.
        * `domain` - The entry matches every email address under the
          given domain.
                :type type: SharedLinkOtpAllowlistEntryTypeField
                :param value: The value of the allowlist entry.

        * For `email` entries, the full email address (must contain `@`).
        * For `domain` entries, the bare domain (e.g. `example.com`).
                :type value: str
                :param created_at: The date and time when the allowlist entry was added.
                :type created_at: DateTime
        """
        super().__init__(**kwargs)
        self.type = type
        self.value = value
        self.created_at = created_at
        self.created_by = created_by
