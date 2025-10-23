from enum import Enum

from box_sdk_gen.box.errors import BoxSDKError


class CollaborationRestrictionV2025R0(str, Enum):
    INTERNAL = 'internal'
    EXTERNAL = 'external'
