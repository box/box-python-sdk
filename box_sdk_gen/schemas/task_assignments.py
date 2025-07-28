from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.task_assignment import TaskAssignment

from box_sdk_gen.box.errors import BoxSDKError


class TaskAssignments(BaseObject):
    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        entries: Optional[List[TaskAssignment]] = None,
        **kwargs
    ):
        """
        :param total_count: The total number of items in this collection., defaults to None
        :type total_count: Optional[int], optional
        :param entries: A list of task assignments., defaults to None
        :type entries: Optional[List[TaskAssignment]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries
