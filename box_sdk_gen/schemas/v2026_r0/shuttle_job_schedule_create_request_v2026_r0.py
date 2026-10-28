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


class ShuttleJobScheduleCreateRequestV2026R0RunModeField(str, Enum):
    TRANSFER = 'transfer'
    SIMULATION = 'simulation'
    ANALYSIS = 'analysis'


class ShuttleJobScheduleCreateRequestV2026R0StateField(str, Enum):
    ENABLED = 'enabled'
    PAUSED = 'paused'


class ShuttleJobScheduleCreateRequestV2026R0(BaseObject):
    def __init__(
        self,
        job_id: str,
        run_mode: ShuttleJobScheduleCreateRequestV2026R0RunModeField,
        trigger: ShuttleJobScheduleTriggerV2026R0,
        *,
        state: Optional[ShuttleJobScheduleCreateRequestV2026R0StateField] = None,
        description: Optional[str] = None,
        **kwargs
    ):
        """
                :param job_id: The unique identifier of the shuttle job this schedule belongs to.
                :type job_id: str
                :param run_mode: The kind of run the schedule starts. `scan` is not a valid schedule
        run mode.
                :type run_mode: ShuttleJobScheduleCreateRequestV2026R0RunModeField
                :param state: Whether the schedule is active. When omitted, defaults to `enabled`., defaults to None
                :type state: Optional[ShuttleJobScheduleCreateRequestV2026R0StateField], optional
                :param description: An optional human-readable description of the schedule., defaults to None
                :type description: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.job_id = job_id
        self.run_mode = run_mode
        self.trigger = trigger
        self.state = state
        self.description = description
