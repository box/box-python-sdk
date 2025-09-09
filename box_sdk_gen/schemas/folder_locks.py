from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.folder_lock import FolderLock

from box_sdk_gen.box.errors import BoxSDKError


class FolderLocks(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[FolderLock]] = None,
        limit: Optional[str] = None,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: A list of folder locks., defaults to None
                :type entries: Optional[List[FolderLock]], optional
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[str], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
        self.next_marker = next_marker
