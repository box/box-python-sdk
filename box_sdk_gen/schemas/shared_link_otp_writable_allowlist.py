from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.shared_link_otp_allowlist_entry_writable import (
    SharedLinkOtpAllowlistEntryWritable,
)

from box_sdk_gen.box.errors import BoxSDKError


class SharedLinkOtpWritableAllowlistModeField(str, Enum):
    ALLOWLIST = 'allowlist'


class SharedLinkOtpWritableAllowlist(BaseObject):
    def __init__(
        self,
        allowlist: List[SharedLinkOtpAllowlistEntryWritable],
        *,
        mode: SharedLinkOtpWritableAllowlistModeField = SharedLinkOtpWritableAllowlistModeField.ALLOWLIST,
        **kwargs
    ):
        """
                :param allowlist: The list of email and domain entries that are permitted to access the
        shared link when `mode` is `allowlist`. Anonymous users whose
        email matches an entry can request and verify a one-time-passcode.

        Providing this field replaces the entire existing allowlist; passing
        an empty array clears all entries. Required when `mode` is `allowlist`.
                :type allowlist: List[SharedLinkOtpAllowlistEntryWritable]
                :param mode: Set to `allowlist` to restrict OTP requests to emails matching an
        entry on the `allowlist`., defaults to SharedLinkOtpWritableAllowlistModeField.ALLOWLIST
                :type mode: SharedLinkOtpWritableAllowlistModeField, optional
        """
        super().__init__(**kwargs)
        self.allowlist = allowlist
        self.mode = mode
