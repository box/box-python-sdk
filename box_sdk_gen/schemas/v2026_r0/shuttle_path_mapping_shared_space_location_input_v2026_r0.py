from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingSharedSpaceLocationInputV2026R0TypeField(str, Enum):
    SHARED_SPACE = 'shared_space'


class ShuttlePathMappingSharedSpaceLocationInputV2026R0(BaseObject):
    _discriminator = 'type', {'shared_space'}

    def __init__(
        self,
        path: str,
        *,
        type: ShuttlePathMappingSharedSpaceLocationInputV2026R0TypeField = ShuttlePathMappingSharedSpaceLocationInputV2026R0TypeField.SHARED_SPACE,
        space: Optional[str] = None,
        path_id: Optional[str] = None,
        is_directory: Optional[bool] = None,
        **kwargs
    ):
        """
                :param path: The human-readable path relative to the shared container.
                :type path: str
                :param type: The value will always be `shared_space`., defaults to ShuttlePathMappingSharedSpaceLocationInputV2026R0TypeField.SHARED_SPACE
                :type type: ShuttlePathMappingSharedSpaceLocationInputV2026R0TypeField, optional
                :param space: The display name of the shared container. Required for systems with
        multiple containers., defaults to None
                :type space: Optional[str], optional
                :param path_id: An optional stable identifier of the location, when obtained from
        browsing., defaults to None
                :type path_id: Optional[str], optional
                :param is_directory: Whether the location is a directory. When set, the destination must be
        the same kind of object., defaults to None
                :type is_directory: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.path = path
        self.type = type
        self.space = space
        self.path_id = path_id
        self.is_directory = is_directory
