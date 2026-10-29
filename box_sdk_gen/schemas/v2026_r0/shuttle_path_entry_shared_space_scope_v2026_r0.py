from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathEntrySharedSpaceScopeV2026R0TypeField(str, Enum):
    SHARED_SPACE = 'shared_space'


class ShuttlePathEntrySharedSpaceScopeV2026R0(BaseObject):
    _discriminator = 'type', {'shared_space'}

    def __init__(
        self,
        *,
        type: ShuttlePathEntrySharedSpaceScopeV2026R0TypeField = ShuttlePathEntrySharedSpaceScopeV2026R0TypeField.SHARED_SPACE,
        space: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `shared_space`., defaults to ShuttlePathEntrySharedSpaceScopeV2026R0TypeField.SHARED_SPACE
                :type type: ShuttlePathEntrySharedSpaceScopeV2026R0TypeField, optional
                :param space: The display name of the shared container this entry belongs to.
        `null` when the system has a single implicit container. Maps to
        `space` on a shared-space path mapping location., defaults to None
                :type space: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.space = space
