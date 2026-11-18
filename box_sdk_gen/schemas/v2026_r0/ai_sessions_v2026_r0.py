from typing import List

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.ai_session_v2026_r0 import AiSessionV2026R0

from box_sdk_gen.box.errors import BoxSDKError


class AiSessionsV2026R0(BaseObject):
    def __init__(
        self,
        entries: List[AiSessionV2026R0],
        limit: int,
        *,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: A list of AI sessions. The list is empty when there are no results.
                :type entries: List[AiSessionV2026R0]
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API.
                :type limit: int
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
        self.next_marker = next_marker
