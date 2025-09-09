from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TaskAssignmentTypeField(str, Enum):
    TASK_ASSIGNMENT = 'task_assignment'


class TaskAssignmentResolutionStateField(str, Enum):
    COMPLETED = 'completed'
    INCOMPLETE = 'incomplete'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class TaskAssignment(BaseObject):
    _discriminator = 'type', {'task_assignment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[TaskAssignmentTypeField] = None,
        item: Optional[FileMini] = None,
        assigned_to: Optional[UserMini] = None,
        message: Optional[str] = None,
        completed_at: Optional[DateTime] = None,
        assigned_at: Optional[DateTime] = None,
        reminded_at: Optional[DateTime] = None,
        resolution_state: Optional[TaskAssignmentResolutionStateField] = None,
        assigned_by: Optional[UserMini] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this task assignment., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `task_assignment`., defaults to None
                :type type: Optional[TaskAssignmentTypeField], optional
                :param message: A message that will is included with the task
        assignment. This is visible to the assigned user in the web and mobile
        UI., defaults to None
                :type message: Optional[str], optional
                :param completed_at: The date at which this task assignment was
        completed. This will be `null` if the task is not completed yet., defaults to None
                :type completed_at: Optional[DateTime], optional
                :param assigned_at: The date at which this task was assigned to the user., defaults to None
                :type assigned_at: Optional[DateTime], optional
                :param reminded_at: The date at which the assigned user was reminded of this task
        assignment., defaults to None
                :type reminded_at: Optional[DateTime], optional
                :param resolution_state: The current state of the assignment. The available states depend on
        the `action` value of the task object., defaults to None
                :type resolution_state: Optional[TaskAssignmentResolutionStateField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.item = item
        self.assigned_to = assigned_to
        self.message = message
        self.completed_at = completed_at
        self.assigned_at = assigned_at
        self.reminded_at = reminded_at
        self.resolution_state = resolution_state
        self.assigned_by = assigned_by
