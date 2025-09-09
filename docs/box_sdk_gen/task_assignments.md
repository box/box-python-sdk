# TaskAssignmentsManager

- [List task assignments](#list-task-assignments)
- [Assign task](#assign-task)
- [Get task assignment](#get-task-assignment)
- [Update task assignment](#update-task-assignment)
- [Unassign task](#unassign-task)

## List task assignments

Lists all of the assignments for a given task.

This operation is performed by calling function `get_task_assignments`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-tasks-id-assignments/).

<!-- sample get_tasks_id_assignments -->

```python
client.task_assignments.get_task_assignments(task.id)
```

### Arguments

- task_id `str`
  - The ID of the task. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TaskAssignments`.

Returns a collection of task assignment defining what task on
a file has been assigned to which users and by who.

## Assign task

Assigns a task to a user.

A task can be assigned to more than one user by creating multiple
assignments.

This operation is performed by calling function `create_task_assignment`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-task-assignments/).

<!-- sample post_task_assignments -->

```python
client.task_assignments.create_task_assignment(CreateTaskAssignmentTask(type=CreateTaskAssignmentTaskTypeField.TASK, id=task.id), CreateTaskAssignmentAssignTo(id=current_user.id))
```

### Arguments

- task `CreateTaskAssignmentTask`
  - The task to assign to a user.
- assign_to `CreateTaskAssignmentAssignTo`
  - The user to assign the task to.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TaskAssignment`.

Returns a new task assignment object.

## Get task assignment

Retrieves information about a task assignment.

This operation is performed by calling function `get_task_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-task-assignments-id/).

<!-- sample get_task_assignments_id -->

```python
client.task_assignments.get_task_assignment_by_id(task_assignment.id)
```

### Arguments

- task_assignment_id `str`
  - The ID of the task assignment. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TaskAssignment`.

Returns a task assignment, specifying who the task has been assigned to
and by whom.

## Update task assignment

Updates a task assignment. This endpoint can be
used to update the state of a task assigned to a user.

This operation is performed by calling function `update_task_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-task-assignments-id/).

<!-- sample put_task_assignments_id -->

```python
client.task_assignments.update_task_assignment_by_id(task_assignment.id, message='updated message', resolution_state=UpdateTaskAssignmentByIdResolutionState.APPROVED)
```

### Arguments

- task_assignment_id `str`
  - The ID of the task assignment. Example: "12345"
- message `Optional[str]`
  - An optional message by the assignee that can be added to the task.
- resolution_state `Optional[UpdateTaskAssignmentByIdResolutionState]`
  - The state of the task assigned to the user. _ For a task with an `action` value of `complete` this can be `incomplete` or `completed`. _ For a task with an `action` of `review` this can be `incomplete`, `approved`, or `rejected`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TaskAssignment`.

Returns the updated task assignment object.

## Unassign task

Deletes a specific task assignment.

This operation is performed by calling function `delete_task_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-task-assignments-id/).

<!-- sample delete_task_assignments_id -->

```python
client.task_assignments.delete_task_assignment_by_id(task_assignment.id)
```

### Arguments

- task_assignment_id `str`
  - The ID of the task assignment. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the task
assignment was successfully deleted.
