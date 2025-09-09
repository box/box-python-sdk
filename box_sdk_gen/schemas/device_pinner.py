from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError


class DevicePinnerTypeField(str, Enum):
    DEVICE_PINNER = 'device_pinner'


class DevicePinner(BaseObject):
    _discriminator = 'type', {'device_pinner'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[DevicePinnerTypeField] = None,
        owned_by: Optional[UserMini] = None,
        product_name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this device pin., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `device_pinner`., defaults to None
        :type type: Optional[DevicePinnerTypeField], optional
        :param product_name: The type of device being pinned., defaults to None
        :type product_name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.owned_by = owned_by
        self.product_name = product_name
