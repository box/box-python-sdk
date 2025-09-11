from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierReportBaseTypeField(str, Enum):
    SHIELD_INFORMATION_BARRIER_REPORT = 'shield_information_barrier_report'


class ShieldInformationBarrierReportBase(BaseObject):
    _discriminator = 'type', {'shield_information_barrier_report'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierReportBaseTypeField] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for the shield information barrier report., defaults to None
        :type id: Optional[str], optional
        :param type: The type of the shield information barrier report., defaults to None
        :type type: Optional[ShieldInformationBarrierReportBaseTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
