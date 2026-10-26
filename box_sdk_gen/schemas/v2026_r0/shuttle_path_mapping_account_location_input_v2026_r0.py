from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_path_mapping_account_input_v2026_r0 import (
    ShuttlePathMappingAccountInputV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingAccountLocationInputV2026R0TypeField(str, Enum):
    ACCOUNT = 'account'


class ShuttlePathMappingAccountLocationInputV2026R0(BaseObject):
    _discriminator = 'type', {'account'}

    def __init__(
        self,
        path: str,
        account: ShuttlePathMappingAccountInputV2026R0,
        *,
        type: ShuttlePathMappingAccountLocationInputV2026R0TypeField = ShuttlePathMappingAccountLocationInputV2026R0TypeField.ACCOUNT,
        path_id: Optional[str] = None,
        is_directory: Optional[bool] = None,
        **kwargs
    ):
        """
                :param path: The human-readable path relative to the account root.
                :type path: str
                :param type: The value will always be `account`., defaults to ShuttlePathMappingAccountLocationInputV2026R0TypeField.ACCOUNT
                :type type: ShuttlePathMappingAccountLocationInputV2026R0TypeField, optional
                :param path_id: An optional stable identifier of the location, when obtained from
        browsing., defaults to None
                :type path_id: Optional[str], optional
                :param is_directory: Whether the location is a directory. When set, the destination must be
        the same kind of object., defaults to None
                :type is_directory: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.path = path
        self.account = account
        self.type = type
        self.path_id = path_id
        self.is_directory = is_directory
