from typing import Union

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_time_v2026_r0 import (
    ShuttleJobScheduleTriggerByTimeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.shuttle_job_schedule_trigger_by_job_v2026_r0 import (
    ShuttleJobScheduleTriggerByJobV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

ShuttleJobScheduleTriggerV2026R0 = Union[
    ShuttleJobScheduleTriggerByTimeV2026R0, ShuttleJobScheduleTriggerByJobV2026R0
]
