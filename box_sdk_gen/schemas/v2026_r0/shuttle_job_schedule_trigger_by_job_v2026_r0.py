from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleJobScheduleTriggerByJobV2026R0TypeField(str, Enum):
    BY_JOB = 'by_job'


class ShuttleJobScheduleTriggerByJobV2026R0LastRunConditionField(str, Enum):
    ALWAYS = 'always'
    ON_SUCCESS = 'on_success'
    ON_FINISH = 'on_finish'


class ShuttleJobScheduleTriggerByJobV2026R0(BaseObject):
    _discriminator = 'type', {'by_job'}

    def __init__(
        self,
        triggered_by_job_id: str,
        last_run_condition: ShuttleJobScheduleTriggerByJobV2026R0LastRunConditionField,
        *,
        type: ShuttleJobScheduleTriggerByJobV2026R0TypeField = ShuttleJobScheduleTriggerByJobV2026R0TypeField.BY_JOB,
        **kwargs
    ):
        """
                :param triggered_by_job_id: The unique identifier of the shuttle job whose run starts this
        schedule.
                :type triggered_by_job_id: str
                :param last_run_condition: When this schedule should start a run relative to the last run of
        the triggering job.
                :type last_run_condition: ShuttleJobScheduleTriggerByJobV2026R0LastRunConditionField
                :param type: The value will always be `by_job`., defaults to ShuttleJobScheduleTriggerByJobV2026R0TypeField.BY_JOB
                :type type: ShuttleJobScheduleTriggerByJobV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.triggered_by_job_id = triggered_by_job_id
        self.last_run_condition = last_run_condition
        self.type = type
