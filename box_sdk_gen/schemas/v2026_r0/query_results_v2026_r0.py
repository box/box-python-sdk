from typing import List

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.query_result_entry_v2026_r0 import (
    QueryResultEntryV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class QueryResultsV2026R0(BaseObject):
    def __init__(
        self,
        entries: List[QueryResultEntryV2026R0],
        limit: int,
        *,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: The list of items matching the query predicate.
                :type entries: List[QueryResultEntryV2026R0]
                :param limit: The limit that was used for this request. This will be the same as the limit query
        parameter unless that value exceeded the maximum value allowed.
                :type limit: int
                :param next_marker: The marker for the start of the next page of results. When `null`, there
        are no further results available., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
        self.next_marker = next_marker
