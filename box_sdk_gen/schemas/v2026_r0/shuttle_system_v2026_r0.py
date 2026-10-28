from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSystemV2026R0TypeField(str, Enum):
    SHUTTLE_SYSTEM = 'shuttle_system'


class ShuttleSystemV2026R0StateField(str, Enum):
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    UNKNOWN = 'unknown'


class ShuttleSystemV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_system'}

    def __init__(
        self,
        id: str,
        name: str,
        system_type: str,
        state: ShuttleSystemV2026R0StateField,
        *,
        type: ShuttleSystemV2026R0TypeField = ShuttleSystemV2026R0TypeField.SHUTTLE_SYSTEM,
        label: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shuttle system.
                :type id: str
                :param name: The display name of the shuttle system.
                :type name: str
                :param system_type: Identifies the kind of source or destination this system represents, for
        example `box`, `windows`, `sharepoint`, or `amazon_s3`. New system types
        are added over time, so clients must tolerate values they do not
        recognize rather than treating this as a fixed set.
                :type system_type: str
                :param state: The current connection state of the shuttle system.
                :type state: ShuttleSystemV2026R0StateField
                :param type: The value will always be `shuttle_system`., defaults to ShuttleSystemV2026R0TypeField.SHUTTLE_SYSTEM
                :type type: ShuttleSystemV2026R0TypeField, optional
                :param label: A server-computed display label for the system., defaults to None
                :type label: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.system_type = system_type
        self.state = state
        self.type = type
        self.label = label
