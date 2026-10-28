from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.shuttle_report_output_v2026_r0 import (
    ShuttleReportOutputV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShuttleReportV2026R0TypeField(str, Enum):
    SHUTTLE_REPORT = 'shuttle_report'


class ShuttleReportV2026R0FormatField(str, Enum):
    XLSX = 'xlsx'
    CSV = 'csv'


class ShuttleReportV2026R0UsersScopeField(str, Enum):
    MIGRATED = 'migrated'
    ALL = 'all'


class ShuttleReportV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_report'}

    def __init__(
        self,
        id: str,
        run_id: str,
        status: str,
        format: ShuttleReportV2026R0FormatField,
        *,
        type: ShuttleReportV2026R0TypeField = ShuttleReportV2026R0TypeField.SHUTTLE_REPORT,
        sections: Optional[List[str]] = None,
        users_scope: Optional[ShuttleReportV2026R0UsersScopeField] = None,
        output: Optional[ShuttleReportOutputV2026R0] = None,
        created_at: Optional[DateTime] = None,
        completed_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shuttle report.
                :type id: str
                :param run_id: The unique identifier of the shuttle run this report was generated
        for.
                :type run_id: str
                :param status: The generation status of the report. This is an open string whose set
        of values is expected to grow; the currently documented values include
        `pending`, `processing`, `complete`, `failed`, `canceled`, and
        `unknown`. Keep polling `pending` and `processing`. Stop on
        `complete`, `failed`, `canceled`, and `unknown`. Treat any value that
        is not recognized the same as `unknown`: do not fail parsing, and do
        not keep polling.
                :type status: str
                :param format: The output file format of the report.
                :type format: ShuttleReportV2026R0FormatField
                :param type: The value will always be `shuttle_report`., defaults to ShuttleReportV2026R0TypeField.SHUTTLE_REPORT
                :type type: ShuttleReportV2026R0TypeField, optional
                :param sections: The sections included in the report. Echoes the sections requested on
        create. This is an open list whose set of values is expected to grow;
        the currently documented values include `files_and_folders`,
        `event_log`, `transfer_overview`, `source_users`, `target_users`,
        `source_collaborators`, `target_collaborators`,
        `source_collaborations`, and `target_collaborations`. Omitted on
        older reports that have no stored section list. New reports always
        include this field., defaults to None
                :type sections: Optional[List[str]], optional
                :param users_scope: Which users are included in user-related report sections., defaults to None
                :type users_scope: Optional[ShuttleReportV2026R0UsersScopeField], optional
                :param output: The generated Box file or folder. Always present; `null` until
        `status` is `complete`., defaults to None
                :type output: Optional[ShuttleReportOutputV2026R0], optional
                :param created_at: When report generation was requested., defaults to None
                :type created_at: Optional[DateTime], optional
                :param completed_at: When report generation finished. Always present; `null` while
        generation is still in progress., defaults to None
                :type completed_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.run_id = run_id
        self.status = status
        self.format = format
        self.type = type
        self.sections = sections
        self.users_scope = users_scope
        self.output = output
        self.created_at = created_at
        self.completed_at = completed_at
