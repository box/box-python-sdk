from typing import Union

from box_sdk_gen.schemas.v2025_r0.hub_collaboration_user_v2025_r0 import (
    HubCollaborationUserV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.group_mini_v2025_r0 import GroupMiniV2025R0

from box_sdk_gen.box.errors import BoxSDKError

HubAccessGranteeV2025R0 = Union[HubCollaborationUserV2025R0, GroupMiniV2025R0]
