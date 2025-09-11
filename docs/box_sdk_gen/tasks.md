# TasksManager

- [List tasks on file](#list-tasks-on-file)
- [Create task](#create-task)
- [Get task](#get-task)
- [Update task](#update-task)
- [Remove task](#remove-task)

## List tasks on file

Retrieves a list of all the tasks for a file. This
endpoint does not support pagination.

This operation is performed by calling function `get_file_tasks`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-tasks/).

<!-- sample get_files_id_tasks -->

```python
client.tasks.get_file_tasks(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Tasks`.

Returns a list of tasks on a file.

If there are no tasks on this file an empty collection is returned
instead.

## Create task

Creates a single task on a file. This task is not assigned to any user and
will need to be assigned separately.

This operation is performed by calling function `create_task`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-tasks/).

<!-- sample post_tasks -->

```python
client.tasks.create_task(CreateTaskItem(type=CreateTaskItemTypeField.FILE, id=file.id), action=CreateTaskAction.REVIEW, message='test message', due_at=date_time, completion_rule=CreateTaskCompletionRule.ALL_ASSIGNEES)
```

### Arguments

- item `CreateTaskItem`
  - The file to attach the task to.
- action `Optional[CreateTaskAction]`
  - The action the task assignee will be prompted to do. Must be _ `review` defines an approval task that can be approved or, rejected _ `complete` defines a general task which can be completed.
- message `Optional[str]`
  - An optional message to include with the task.
- due_at `Optional[DateTime]`
  - Defines when the task is due. Defaults to `null` if not provided.
- completion_rule `Optional[CreateTaskCompletionRule]`
  - Defines which assignees need to complete this task before the task is considered completed. _ `all_assignees` (default) requires all assignees to review or approve the task in order for it to be considered completed. _ `any_assignee` accepts any one assignee to review or approve the task in order for it to be considered completed.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Task`.

Returns the newly created task.

## Get task

Retrieves information about a specific task.

This operation is performed by calling function `get_task_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-tasks-id/).

<!-- sample get_tasks_id -->

```python
client.tasks.get_task_by_id(task.id)
```

### Arguments

- task_id `str`
  - The ID of the task. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Task`.

Returns a task object.

## Update task

Updates a task. This can be used to update a task's configuration, or to
update its completion state.

This operation is performed by calling function `update_task_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-tasks-id/).

<!-- sample put_tasks_id -->

```python
client.tasks.update_task_by_id(task.id, message='updated message')
```

### Arguments

- task_id `str`
  - The ID of the task. Example: "12345"
- action `Optional[UpdateTaskByIdAction]`
  - The action the task assignee will be prompted to do. Must be _ `review` defines an approval task that can be approved or rejected, _ `complete` defines a general task which can be completed.
- message `Optional[str]`
  - The message included with the task.
- due_at `Optional[DateTime]`
  - When the task is due at.
- completion_rule `Optional[UpdateTaskByIdCompletionRule]`
  - Defines which assignees need to complete this task before the task is considered completed. _ `all_assignees` (default) requires all assignees to review or approve the task in order for it to be considered completed. _ `any_assignee` accepts any one assignee to review or approve the task in order for it to be considered completed.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Task`.

Returns the updated task object.

## Remove task

Removes a task from a file.

This operation is performed by calling function `delete_task_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-tasks-id/).

<!-- sample delete_tasks_id -->

```python
client.tasks.delete_task_by_id(task.id)
```

### Arguments

- task_id `str`
  - The ID of the task. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the task was successfully deleted.
