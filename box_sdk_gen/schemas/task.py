from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.task_assignments import TaskAssignments

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TaskTypeField(str, Enum):
    TASK = 'task'


class TaskActionField(str, Enum):
    REVIEW = 'review'
    COMPLETE = 'complete'


class TaskCompletionRuleField(str, Enum):
    ALL_ASSIGNEES = 'all_assignees'
    ANY_ASSIGNEE = 'any_assignee'


class Task(BaseObject):
    _discriminator = 'type', {'task'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[TaskTypeField] = None,
        item: Optional[FileMini] = None,
        due_at: Optional[DateTime] = None,
        action: Optional[TaskActionField] = None,
        message: Optional[str] = None,
        task_assignment_collection: Optional[TaskAssignments] = None,
        is_completed: Optional[bool] = None,
        created_by: Optional[UserMini] = None,
        created_at: Optional[DateTime] = None,
        completion_rule: Optional[TaskCompletionRuleField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this task., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `task`., defaults to None
                :type type: Optional[TaskTypeField], optional
                :param due_at: When the task is due., defaults to None
                :type due_at: Optional[DateTime], optional
                :param action: The type of task the task assignee will be prompted to
        perform., defaults to None
                :type action: Optional[TaskActionField], optional
                :param message: A message that will be included with the task., defaults to None
                :type message: Optional[str], optional
                :param is_completed: Whether the task has been completed., defaults to None
                :type is_completed: Optional[bool], optional
                :param created_at: When the task object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param completion_rule: Defines which assignees need to complete this task before the task
        is considered completed.

        * `all_assignees` requires all assignees to review or
        approve the task in order for it to be considered completed.
        * `any_assignee` accepts any one assignee to review or
        approve the task in order for it to be considered completed., defaults to None
                :type completion_rule: Optional[TaskCompletionRuleField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.item = item
        self.due_at = due_at
        self.action = action
        self.message = message
        self.task_assignment_collection = task_assignment_collection
        self.is_completed = is_completed
        self.created_by = created_by
        self.created_at = created_at
        self.completion_rule = completion_rule
