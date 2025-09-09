from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class TrackingCodeTypeField(str, Enum):
    TRACKING_CODE = 'tracking_code'


class TrackingCode(BaseObject):
    _discriminator = 'type', {'tracking_code'}

    def __init__(
        self,
        *,
        type: Optional[TrackingCodeTypeField] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `tracking_code`., defaults to None
                :type type: Optional[TrackingCodeTypeField], optional
                :param name: The name of the tracking code, which must be preconfigured in
        the Admin Console., defaults to None
                :type name: Optional[str], optional
                :param value: The value of the tracking code., defaults to None
                :type value: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.name = name
        self.value = value
