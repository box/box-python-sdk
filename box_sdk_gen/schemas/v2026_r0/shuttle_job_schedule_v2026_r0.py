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

from box_sdk_gen.internal.utils import DateTime


class ShuttleJobScheduleV2026R0TypeField(str, Enum):
    SHUTTLE_JOB_SCHEDULE = 'shuttle_job_schedule'


class ShuttleJobScheduleV2026R0StateField(str, Enum):
    ENABLED = 'enabled'
    PAUSED = 'paused'


class ShuttleJobScheduleV2026R0RunModeField(str, Enum):
    TRANSFER = 'transfer'
    SIMULATION = 'simulation'
    ANALYSIS = 'analysis'


class ShuttleJobScheduleV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_job_schedule'}

    def __init__(
        self,
        id: str,
        job_id: str,
        state: ShuttleJobScheduleV2026R0StateField,
        run_mode: ShuttleJobScheduleV2026R0RunModeField,
        trigger: ShuttleJobScheduleTriggerV2026R0,
        *,
        type: ShuttleJobScheduleV2026R0TypeField = ShuttleJobScheduleV2026R0TypeField.SHUTTLE_JOB_SCHEDULE,
        description: Optional[str] = None,
        last_attempt_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shuttle job schedule.
                :type id: str
                :param job_id: The unique identifier of the shuttle job this schedule belongs to.
                :type job_id: str
                :param state: Whether the schedule is active.
                :type state: ShuttleJobScheduleV2026R0StateField
                :param run_mode: The kind of run the schedule starts. `scan` is not a valid schedule
        run mode.
                :type run_mode: ShuttleJobScheduleV2026R0RunModeField
                :param type: The value will always be `shuttle_job_schedule`., defaults to ShuttleJobScheduleV2026R0TypeField.SHUTTLE_JOB_SCHEDULE
                :type type: ShuttleJobScheduleV2026R0TypeField, optional
                :param description: An optional human-readable description of the schedule., defaults to None
                :type description: Optional[str], optional
                :param last_attempt_at: When the schedule last attempted to start a run. `null` when the
        schedule has never started a run., defaults to None
                :type last_attempt_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.job_id = job_id
        self.state = state
        self.run_mode = run_mode
        self.trigger = trigger
        self.type = type
        self.description = description
        self.last_attempt_at = last_attempt_at
