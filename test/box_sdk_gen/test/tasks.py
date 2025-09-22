from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.task import Task

from box_sdk_gen.managers.tasks import CreateTaskItem

from box_sdk_gen.managers.tasks import CreateTaskItemTypeField

from box_sdk_gen.managers.tasks import CreateTaskAction

from box_sdk_gen.managers.tasks import CreateTaskCompletionRule

from box_sdk_gen.schemas.tasks import Tasks

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import date_time_from_string

from box_sdk_gen.internal.utils import date_time_to_string

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testCreateUpdateGetDeleteTask():
    files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(10),
    )
    file: FileFull = files.entries[0]
    date_time: DateTime = date_time_from_string('2035-01-01T00:00:00Z')
    task: Task = client.tasks.create_task(
        CreateTaskItem(type=CreateTaskItemTypeField.FILE, id=file.id),
        action=CreateTaskAction.REVIEW,
        message='test message',
        due_at=date_time,
        completion_rule=CreateTaskCompletionRule.ALL_ASSIGNEES,
    )
    assert task.message == 'test message'
    assert task.item.id == file.id
    assert date_time_to_string(task.due_at) == date_time_to_string(date_time)
    task_by_id: Task = client.tasks.get_task_by_id(task.id)
    assert task_by_id.id == task.id
    task_on_file: Tasks = client.tasks.get_file_tasks(file.id)
    assert task_on_file.total_count == 1
    updated_task: Task = client.tasks.update_task_by_id(
        task.id, message='updated message'
    )
    assert updated_task.message == 'updated message'
    client.tasks.delete_task_by_id(task.id)
    client.files.delete_file_by_id(file.id)
