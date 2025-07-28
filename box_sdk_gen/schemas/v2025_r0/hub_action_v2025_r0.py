from enum import Enum

from box_sdk_gen.box.errors import BoxSDKError


class HubActionV2025R0(str, Enum):
    ADD = 'add'
    REMOVE = 'remove'
