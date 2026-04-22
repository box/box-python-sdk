from enum import Enum

from typing import Union

from box_sdk_gen.box.errors import BoxSDKError


class RetentionPolicyMaxExtensionLengthResponseEnum(str, Enum):
    NONE = 'none'


RetentionPolicyMaxExtensionLengthResponse = Union[
    RetentionPolicyMaxExtensionLengthResponseEnum, str
]
