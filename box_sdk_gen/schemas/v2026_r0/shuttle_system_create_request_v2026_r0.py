from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSystemCreateRequestV2026R0SystemTypeField(str, Enum):
    WINDOWS = 'windows'


class ShuttleSystemCreateRequestV2026R0(BaseObject):
    def __init__(
        self,
        name: str,
        *,
        system_type: ShuttleSystemCreateRequestV2026R0SystemTypeField = ShuttleSystemCreateRequestV2026R0SystemTypeField.WINDOWS,
        **kwargs
    ):
        """
                :param name: The display name for the new shuttle system.
                :type name: str
                :param system_type: The public system type identifier for the new shuttle system. Only
        `windows` is currently supported through the public API., defaults to ShuttleSystemCreateRequestV2026R0SystemTypeField.WINDOWS
                :type system_type: ShuttleSystemCreateRequestV2026R0SystemTypeField, optional
        """
        super().__init__(**kwargs)
        self.name = name
        self.system_type = system_type
