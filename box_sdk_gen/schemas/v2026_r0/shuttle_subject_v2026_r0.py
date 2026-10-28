from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_subject_role_v2026_r0 import (
    ShuttleSubjectRoleV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSubjectV2026R0TypeField(str, Enum):
    USER = 'user'
    GROUP = 'group'


class ShuttleSubjectV2026R0(BaseObject):
    _discriminator = 'type', {'user', 'group'}

    def __init__(
        self,
        type: ShuttleSubjectV2026R0TypeField,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        roles: Optional[List[ShuttleSubjectRoleV2026R0]] = None,
        **kwargs
    ):
        """
                :param type: Whether this subject is a user or a group.
                :type type: ShuttleSubjectV2026R0TypeField
                :param id: The platform-native identifier of the subject. `null` when the system
        does not provide one., defaults to None
                :type id: Optional[str], optional
                :param email: The email address of the subject. `null` when unknown., defaults to None
                :type email: Optional[str], optional
                :param name: The display name of the subject. `null` when unknown., defaults to None
                :type name: Optional[str], optional
                :param roles: Roles this subject holds on the source. `null` when no roles are known., defaults to None
                :type roles: Optional[List[ShuttleSubjectRoleV2026R0]], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.email = email
        self.name = name
        self.roles = roles
