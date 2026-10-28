from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_v2026_r0 import (
    ShuttlePathMappingAccountV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingAccountLocationV2026R0TypeField(str, Enum):
    ACCOUNT = 'account'


class ShuttlePathMappingAccountLocationV2026R0(BaseObject):
    _discriminator = 'type', {'account'}

    def __init__(
        self,
        path: str,
        *,
        type: ShuttlePathMappingAccountLocationV2026R0TypeField = ShuttlePathMappingAccountLocationV2026R0TypeField.ACCOUNT,
        path_id: Optional[str] = None,
        account: Optional[ShuttlePathMappingAccountV2026R0] = None,
        is_directory: Optional[bool] = None,
        **kwargs
    ):
        """
                :param path: The human-readable path relative to the account root.
                :type path: str
                :param type: The value will always be `account`., defaults to ShuttlePathMappingAccountLocationV2026R0TypeField.ACCOUNT
                :type type: ShuttlePathMappingAccountLocationV2026R0TypeField, optional
                :param path_id: The stable identifier of the location. `null` when the system does not
        provide one., defaults to None
                :type path_id: Optional[str], optional
                :param is_directory: Whether the location is a directory. `null` when unknown., defaults to None
                :type is_directory: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.path = path
        self.type = type
        self.path_id = path_id
        self.account = account
        self.is_directory = is_directory
