from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleTargetSubjectV2026R0TypeField(str, Enum):
    USER = 'user'
    GROUP = 'group'


class ShuttleTargetSubjectV2026R0(BaseObject):
    _discriminator = 'type', {'user', 'group'}

    def __init__(
        self,
        type: ShuttleTargetSubjectV2026R0TypeField,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: Whether the Box target is a user or a group.
                :type type: ShuttleTargetSubjectV2026R0TypeField
                :param id: The Box user or group ID. `null` when the mapping was not created
        through this API and is identified by email (user) or name (group)
        instead. Skip is represented by `target: null`, not a missing `id`.
        Create and update always send `id`., defaults to None
                :type id: Optional[str], optional
                :param email: The email address of the target. `null` when unknown., defaults to None
                :type email: Optional[str], optional
                :param name: The display name of the target. `null` when unknown., defaults to None
                :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.email = email
        self.name = name
