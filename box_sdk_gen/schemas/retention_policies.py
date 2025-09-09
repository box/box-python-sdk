from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.retention_policy import RetentionPolicy

from box_sdk_gen.box.errors import BoxSDKError


class RetentionPolicies(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[RetentionPolicy]] = None,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: A list in which each entry represents a retention policy object., defaults to None
                :type entries: Optional[List[RetentionPolicy]], optional
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
