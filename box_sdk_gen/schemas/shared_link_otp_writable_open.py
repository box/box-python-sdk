from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SharedLinkOtpWritableOpenModeField(str, Enum):
    OPEN = 'open'


class SharedLinkOtpWritableOpen(BaseObject):
    def __init__(
        self,
        *,
        mode: SharedLinkOtpWritableOpenModeField = SharedLinkOtpWritableOpenModeField.OPEN,
        **kwargs
    ):
        """
                :param mode: Set to `open` to allow any anonymous recipient to request a
        one-time-passcode to any email address., defaults to SharedLinkOtpWritableOpenModeField.OPEN
                :type mode: SharedLinkOtpWritableOpenModeField, optional
        """
        super().__init__(**kwargs)
        self.mode = mode
