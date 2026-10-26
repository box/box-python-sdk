from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.v2026_r0.user_base_v2026_r0 import UserBaseV2026R0

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShuttleRunV2026R0TypeField(str, Enum):
    SHUTTLE_RUN = 'shuttle_run'


class ShuttleRunV2026R0StatsField(BaseObject):
    def __init__(
        self,
        *,
        bytes_sent: Optional[int] = None,
        files_sent: Optional[int] = None,
        folders_created: Optional[int] = None,
        is_estimated: Optional[bool] = None,
        **kwargs
    ):
        """
        :param bytes_sent: Bytes transferred during the run., defaults to None
        :type bytes_sent: Optional[int], optional
        :param files_sent: Files transferred during the run., defaults to None
        :type files_sent: Optional[int], optional
        :param folders_created: Folders created on the destination during the run., defaults to None
        :type folders_created: Optional[int], optional
        :param is_estimated: Whether these figures are estimates rather than final counts., defaults to None
        :type is_estimated: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.bytes_sent = bytes_sent
        self.files_sent = files_sent
        self.folders_created = folders_created
        self.is_estimated = is_estimated


class ShuttleRunV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_run'}

    def __init__(
        self,
        id: str,
        job_id: str,
        run_mode: str,
        state: str,
        *,
        type: ShuttleRunV2026R0TypeField = ShuttleRunV2026R0TypeField.SHUTTLE_RUN,
        started_at: Optional[DateTime] = None,
        ended_at: Optional[DateTime] = None,
        duration_seconds: Optional[int] = None,
        stats: Optional[ShuttleRunV2026R0StatsField] = None,
        created_by: Optional[UserBaseV2026R0] = None,
        available_report_sections: Optional[List[str]] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shuttle run, in the form
        `{job_id}:{run_number}`.
                :type id: str
                :param job_id: The unique identifier of the shuttle job this run belongs to.
                :type job_id: str
                :param run_mode: The mode the run was started in. This is an open string whose set of
        values is expected to grow; the currently documented values include
        `transfer`, `simulation`, `analysis`, `scan`, and `unknown`. Clients
        should treat any value they do not recognize as `unknown`.
                :type run_mode: str
                :param state: The current state of the shuttle run. This is an open string whose set
        of values is expected to grow; the currently documented values include
        `running`, `stopping`, `completed`, `completed_with_errors`, `stopped`,
        `failed`, `timed_out`, and `unknown`. Clients should treat any value
        they do not recognize as `unknown`.
                :type state: str
                :param type: The value will always be `shuttle_run`., defaults to ShuttleRunV2026R0TypeField.SHUTTLE_RUN
                :type type: ShuttleRunV2026R0TypeField, optional
                :param started_at: When the run started., defaults to None
                :type started_at: Optional[DateTime], optional
                :param ended_at: When the run ended. `null` while the run is still in progress., defaults to None
                :type ended_at: Optional[DateTime], optional
                :param duration_seconds: Total duration of the run in seconds. `null` while the run is still in
        progress., defaults to None
                :type duration_seconds: Optional[int], optional
                :param stats: Transfer statistics collected during the run., defaults to None
                :type stats: Optional[ShuttleRunV2026R0StatsField], optional
                :param created_by: The user who started the run. `null` for schedule- or system-initiated
        runs., defaults to None
                :type created_by: Optional[UserBaseV2026R0], optional
                :param available_report_sections: Report sections that can be requested for this run. This is an open
        list whose set of values is expected to grow; the currently documented
        values include `files_and_folders`, `event_log`, `transfer_overview`,
        `source_users`, `target_users`, `source_collaborators`,
        `target_collaborators`, `source_collaborations`, and
        `target_collaborations`., defaults to None
                :type available_report_sections: Optional[List[str]], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.job_id = job_id
        self.run_mode = run_mode
        self.state = state
        self.type = type
        self.started_at = started_at
        self.ended_at = ended_at
        self.duration_seconds = duration_seconds
        self.stats = stats
        self.created_by = created_by
        self.available_report_sections = available_report_sections
