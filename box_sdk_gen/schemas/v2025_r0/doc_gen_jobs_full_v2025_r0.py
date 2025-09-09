from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_full_v2025_r0 import DocGenJobFullV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class DocGenJobsFullV2025R0(BaseObject):
    def __init__(
        self,
        *,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        prev_marker: Optional[str] = None,
        entries: Optional[List[DocGenJobFullV2025R0]] = None,
        **kwargs
    ):
        """
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
                :param prev_marker: The marker for the start of the previous page of results., defaults to None
                :type prev_marker: Optional[str], optional
                :param entries: List of jobs., defaults to None
                :type entries: Optional[List[DocGenJobFullV2025R0]], optional
        """
        super().__init__(**kwargs)
        self.limit = limit
        self.next_marker = next_marker
        self.prev_marker = prev_marker
        self.entries = entries
