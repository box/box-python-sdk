from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleJobScheduleTriggerByTimeV2026R0TypeField(str, Enum):
    BY_TIME = 'by_time'


class ShuttleJobScheduleTriggerByTimeV2026R0RepeatField(str, Enum):
    NONE = 'none'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    WEEKDAYS = 'weekdays'
    WEEKENDS = 'weekends'


class ShuttleJobScheduleTriggerByTimeV2026R0(BaseObject):
    _discriminator = 'type', {'by_time'}

    def __init__(
        self,
        start_at: str,
        time_zone: str,
        repeat: ShuttleJobScheduleTriggerByTimeV2026R0RepeatField,
        *,
        type: ShuttleJobScheduleTriggerByTimeV2026R0TypeField = ShuttleJobScheduleTriggerByTimeV2026R0TypeField.BY_TIME,
        **kwargs
    ):
        """
                :param start_at: The local wall-clock time when the schedule should first start a
        run, without an offset or `Z` suffix. Combined with `time_zone` to
        determine the instant, including DST.
                :type start_at: str
                :param time_zone: The IANA time zone that gives `start_at` its calendar meaning (for
        example `America/Los_Angeles`). Recurrence and DST transitions are
        evaluated in this zone.
                :type time_zone: str
                :param repeat: How often the schedule repeats after `start_at`.
                :type repeat: ShuttleJobScheduleTriggerByTimeV2026R0RepeatField
                :param type: The value will always be `by_time`., defaults to ShuttleJobScheduleTriggerByTimeV2026R0TypeField.BY_TIME
                :type type: ShuttleJobScheduleTriggerByTimeV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.start_at = start_at
        self.time_zone = time_zone
        self.repeat = repeat
        self.type = type
