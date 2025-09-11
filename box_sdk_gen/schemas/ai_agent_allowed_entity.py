from typing import Union

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.schemas.group_base import GroupBase

from box_sdk_gen.box.errors import BoxSDKError

AiAgentAllowedEntity = Union[UserBase, GroupBase]
