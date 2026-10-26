from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_time_v2026_r0 import (
    ShuttleJobScheduleTriggerByTimeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_job_v2026_r0 import (
    ShuttleJobScheduleTriggerByJobV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_v2026_r0 import (
    ShuttleJobScheduleTriggerV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleJobScheduleUpdateRequestV2026R0StateField(str, Enum):
    ENABLED = 'enabled'
    PAUSED = 'paused'


class ShuttleJobScheduleUpdateRequestV2026R0RunModeField(str, Enum):
    TRANSFER = 'transfer'
    SIMULATION = 'simulation'
    ANALYSIS = 'analysis'


class ShuttleJobScheduleUpdateRequestV2026R0(BaseObject):
    def __init__(
        self,
        *,
        state: Optional[ShuttleJobScheduleUpdateRequestV2026R0StateField] = None,
        run_mode: Optional[ShuttleJobScheduleUpdateRequestV2026R0RunModeField] = None,
        description: Optional[str] = None,
        trigger: Optional[ShuttleJobScheduleTriggerV2026R0] = None,
        **kwargs
    ):
        """
                :param state: Whether the schedule is active., defaults to None
                :type state: Optional[ShuttleJobScheduleUpdateRequestV2026R0StateField], optional
                :param run_mode: The kind of run the schedule starts. `scan` is not a valid schedule
        run mode., defaults to None
                :type run_mode: Optional[ShuttleJobScheduleUpdateRequestV2026R0RunModeField], optional
                :param description: An optional human-readable description of the schedule., defaults to None
                :type description: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.state = state
        self.run_mode = run_mode
        self.description = description
        self.trigger = trigger
