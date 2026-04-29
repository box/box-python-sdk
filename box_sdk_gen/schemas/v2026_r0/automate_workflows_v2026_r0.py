from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.automate_workflow_action_v2026_r0 import (
    AutomateWorkflowActionV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class AutomateWorkflowsV2026R0(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[AutomateWorkflowActionV2026R0]] = None,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: Workflow actions available for manual start., defaults to None
                :type entries: Optional[List[AutomateWorkflowActionV2026R0]], optional
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
        self.next_marker = next_marker
