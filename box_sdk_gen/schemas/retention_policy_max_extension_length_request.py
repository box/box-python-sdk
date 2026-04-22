from enum import Enum

from typing import Union

from box_sdk_gen.box.errors import BoxSDKError


class RetentionPolicyMaxExtensionLengthRequestEnum(str, Enum):
    NONE = 'none'


RetentionPolicyMaxExtensionLengthRequest = Union[
    RetentionPolicyMaxExtensionLengthRequestEnum, str, int
]
