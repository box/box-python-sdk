from typing import Union

from box_sdk_gen.schemas.user_collaborations import UserCollaborations

from box_sdk_gen.schemas.group_mini import GroupMini

from box_sdk_gen.box.errors import BoxSDKError

CollaborationAccessGrantee = Union[UserCollaborations, GroupMini]
