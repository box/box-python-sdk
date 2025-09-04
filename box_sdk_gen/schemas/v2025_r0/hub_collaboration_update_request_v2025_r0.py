from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubCollaborationUpdateRequestV2025R0(BaseObject):
    def __init__(self, *, role: Optional[str] = None, **kwargs):
        """
                :param role: The level of access granted to a Box Hub.
        Possible values are `editor`, `viewer`, and `co-owner`., defaults to None
                :type role: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.role = role
