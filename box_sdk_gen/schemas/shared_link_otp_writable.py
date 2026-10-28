from typing import Union

from box_sdk_gen.schemas.shared_link_otp_writable_none import SharedLinkOtpWritableNone

from box_sdk_gen.schemas.shared_link_otp_writable_open import SharedLinkOtpWritableOpen

from box_sdk_gen.schemas.shared_link_otp_writable_allowlist import (
    SharedLinkOtpWritableAllowlist,
)

from box_sdk_gen.box.errors import BoxSDKError

SharedLinkOtpWritable = Union[
    SharedLinkOtpWritableNone, SharedLinkOtpWritableOpen, SharedLinkOtpWritableAllowlist
]
