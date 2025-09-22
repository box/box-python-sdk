from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.task import Task

from box_sdk_gen.managers.tasks import CreateTaskItem

from box_sdk_gen.managers.tasks import CreateTaskItemTypeField

from box_sdk_gen.managers.tasks import CreateTaskAction

from box_sdk_gen.managers.tasks import CreateTaskCompletionRule

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.task_assignment import TaskAssignment

from box_sdk_gen.managers.task_assignments import CreateTaskAssignmentTask

from box_sdk_gen.managers.task_assignments import CreateTaskAssignmentTaskTypeField

from box_sdk_gen.managers.task_assignments import CreateTaskAssignmentAssignTo

from box_sdk_gen.schemas.task_assignments import TaskAssignments

from box_sdk_gen.managers.task_assignments import (
    UpdateTaskAssignmentByIdResolutionState,
)

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.internal.utils import date_time_from_string

client: BoxClient = get_default_client()


def testCreateUpdateGetDeleteTaskAssignment():
    file: FileFull = upload_new_file()
    date: DateTime = date_time_from_string('2035-01-01T00:00:00Z')
    task: Task = client.tasks.create_task(
        CreateTaskItem(type=CreateTaskItemTypeField.FILE, id=file.id),
        action=CreateTaskAction.REVIEW,
        message='test message',
        due_at=date,
        completion_rule=CreateTaskCompletionRule.ALL_ASSIGNEES,
    )
    assert task.message == 'test message'
    assert task.item.id == file.id
    current_user: UserFull = client.users.get_user_me()
    task_assignment: TaskAssignment = client.task_assignments.create_task_assignment(
        CreateTaskAssignmentTask(
            type=CreateTaskAssignmentTaskTypeField.TASK, id=task.id
        ),
        CreateTaskAssignmentAssignTo(id=current_user.id),
    )
    assert task_assignment.item.id == file.id
    assert task_assignment.assigned_to.id == current_user.id
    task_assignment_by_id: TaskAssignment = (
        client.task_assignments.get_task_assignment_by_id(task_assignment.id)
    )
    assert task_assignment_by_id.id == task_assignment.id
    task_assignments_on_task: TaskAssignments = (
        client.task_assignments.get_task_assignments(task.id)
    )
    assert task_assignments_on_task.total_count == 1
    updated_task_assignment: TaskAssignment = (
        client.task_assignments.update_task_assignment_by_id(
            task_assignment.id,
            message='updated message',
            resolution_state=UpdateTaskAssignmentByIdResolutionState.APPROVED,
        )
    )
    assert updated_task_assignment.message == 'updated message'
    assert to_string(updated_task_assignment.resolution_state) == 'approved'
    with pytest.raises(Exception):
        client.task_assignments.delete_task_assignment_by_id(task_assignment.id)
    client.files.delete_file_by_id(file.id)
