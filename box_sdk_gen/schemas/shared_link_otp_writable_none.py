from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SharedLinkOtpWritableNoneModeField(str, Enum):
    NONE = 'none'


class SharedLinkOtpWritableNone(BaseObject):
    def __init__(
        self,
        *,
        mode: SharedLinkOtpWritableNoneModeField = SharedLinkOtpWritableNoneModeField.NONE,
        **kwargs
    ):
        """
        :param mode: Set to `none` to disable OTP enforcement for the shared link., defaults to SharedLinkOtpWritableNoneModeField.NONE
        :type mode: SharedLinkOtpWritableNoneModeField, optional
        """
        super().__init__(**kwargs)
        self.mode = mode
