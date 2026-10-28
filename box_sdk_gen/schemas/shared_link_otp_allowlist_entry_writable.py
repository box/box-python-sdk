from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SharedLinkOtpAllowlistEntryWritableTypeField(str, Enum):
    EMAIL = 'email'
    DOMAIN = 'domain'


class SharedLinkOtpAllowlistEntryWritable(BaseObject):
    _discriminator = 'type', {'email', 'domain'}

    def __init__(
        self, type: SharedLinkOtpAllowlistEntryWritableTypeField, value: str, **kwargs
    ):
        """
                :param type: The kind of allowlist entry.

        * `email` - The entry matches a single email address.
        * `domain` - The entry matches every email address under the
          given domain.
                :type type: SharedLinkOtpAllowlistEntryWritableTypeField
                :param value: The value of the allowlist entry.

        * For `email` entries, the full email address (must contain `@`).
        * For `domain` entries, the bare domain (e.g. `example.com`).
                :type value: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.value = value
