from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleJobStartRequestV2026R0ModeField(str, Enum):
    TRANSFER = 'transfer'
    SIMULATION = 'simulation'
    SCAN = 'scan'
    ANALYSIS = 'analysis'


class ShuttleJobStartRequestV2026R0(BaseObject):
    def __init__(
        self, *, mode: Optional[ShuttleJobStartRequestV2026R0ModeField] = None, **kwargs
    ):
        """
        :param mode: The run mode. Defaults to simulation when omitted., defaults to None
        :type mode: Optional[ShuttleJobStartRequestV2026R0ModeField], optional
        """
        super().__init__(**kwargs)
        self.mode = mode
