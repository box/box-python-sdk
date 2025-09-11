from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.shield_information_barrier_report_base import (
    ShieldInformationBarrierReportBaseTypeField,
)

from box_sdk_gen.schemas.shield_information_barrier_report_base import (
    ShieldInformationBarrierReportBase,
)

from box_sdk_gen.schemas.shield_information_barrier_reference import (
    ShieldInformationBarrierReference,
)

from box_sdk_gen.schemas.shield_information_barrier_report_details import (
    ShieldInformationBarrierReportDetails,
)

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShieldInformationBarrierReportStatusField(str, Enum):
    PENDING = 'pending'
    ERROR = 'error'
    DONE = 'done'
    CANCELLED = 'cancelled'


class ShieldInformationBarrierReport(ShieldInformationBarrierReportBase):
    def __init__(
        self,
        *,
        shield_information_barrier: Optional[ShieldInformationBarrierReference] = None,
        status: Optional[ShieldInformationBarrierReportStatusField] = None,
        details: Optional[ShieldInformationBarrierReportDetails] = None,
        created_at: Optional[DateTime] = None,
        created_by: Optional[UserBase] = None,
        updated_at: Optional[DateTime] = None,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierReportBaseTypeField] = None,
        **kwargs
    ):
        """
                :param status: Status of the shield information report., defaults to None
                :type status: Optional[ShieldInformationBarrierReportStatusField], optional
                :param created_at: ISO date time string when this
        shield information barrier report object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param updated_at: ISO date time string when this
        shield information barrier report was updated., defaults to None
                :type updated_at: Optional[DateTime], optional
                :param id: The unique identifier for the shield information barrier report., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier report., defaults to None
                :type type: Optional[ShieldInformationBarrierReportBaseTypeField], optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.shield_information_barrier = shield_information_barrier
        self.status = status
        self.details = details
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
