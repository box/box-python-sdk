from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.task import Task

from box_sdk_gen.box.errors import BoxSDKError


class Tasks(BaseObject):
    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        entries: Optional[List[Task]] = None,
        **kwargs
    ):
        """
                :param total_count: One greater than the offset of the last entry in the entire collection.
        The total number of entries in the collection may be less than
        `total_count`., defaults to None
                :type total_count: Optional[int], optional
                :param entries: A list of tasks., defaults to None
                :type entries: Optional[List[Task]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries
