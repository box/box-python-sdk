from enum import Enum

from typing import List

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleReportCreateRequestV2026R0FormatField(str, Enum):
    XLSX = 'xlsx'
    CSV = 'csv'


class ShuttleReportCreateRequestV2026R0UsersScopeField(str, Enum):
    MIGRATED = 'migrated'
    ALL = 'all'


class ShuttleReportCreateRequestV2026R0(BaseObject):
    def __init__(
        self,
        run_id: str,
        format: ShuttleReportCreateRequestV2026R0FormatField,
        sections: List[str],
        *,
        users_scope: Optional[ShuttleReportCreateRequestV2026R0UsersScopeField] = None,
        **kwargs
    ):
        """
                :param run_id: The unique identifier of the shuttle run to generate a report for.
                :type run_id: str
                :param format: The output file format of the report.
                :type format: ShuttleReportCreateRequestV2026R0FormatField
                :param sections: The sections to include in the report. Must be a non-empty subset of
        the run's `available_report_sections`. This is an open list whose set
        of values is expected to grow; the currently documented values include
        `files_and_folders`, `event_log`, `transfer_overview`, `source_users`,
        `target_users`, `source_collaborators`, `target_collaborators`,
        `source_collaborations`, and `target_collaborations`.
                :type sections: List[str]
                :param users_scope: Which users to include in user-related report sections. Defaults to
        `migrated` when omitted., defaults to None
                :type users_scope: Optional[ShuttleReportCreateRequestV2026R0UsersScopeField], optional
        """
        super().__init__(**kwargs)
        self.run_id = run_id
        self.format = format
        self.sections = sections
        self.users_scope = users_scope
