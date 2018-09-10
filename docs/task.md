Tasks
=====

Task objects represent a user-created task on a file.


Get a Task's Information
------------------------

Calling `task.get()` will return information about the specified task.

```python
task_id = '1234'
task_info = client.task(task_id).get()
```

List Tasks on File
------------------

To retrieve all tasks for a given file use, `file.tasks(limit=None, marker=None, fields=None)`.

```python
file_id = '1111'
tasks = client.file(file_id).tasks()
for task in tasks:
    # Do something
```

Add Task to File
----------------

To create a single task for a single user on a single file use, `file.createtask(message=None, due_at=None)`

```python
file_id = '1111'
task = client.file(file_id).create_task()
```

To specify a message and a due time use

```python
file_id = '1111'
message = 'Please review this'
due_at = "2014-04-03T11:09:43-07:00"
task = client.file(file_id).create_task(message, due_at)
```

Update Task Info
----------------

To update the task information use, `task.update_info()`

```python
task_id = '1234'
task_update = {'message': 'New Message', 'due_at': '2014-04-03T11:09:43-10:00',}
updated_task = client.task(task_id).update_info(task_update)
```

Delete a Task
-------------

To delete a task, use `task.delete()`

```python
task_id = '1234'
client.client.task(task_id).delete()
```

Assign a Task
--------------

To assign a task to a user on a file use. `task.assign(assign_to_id=None, assign_to_login=None)`

```python
task_id = '1234'
assignee_id = '1111'
assignment = client.task(task_id).assign(assignee_id)
```


List Task Assignments
---------------------

To retrieve all task assignments for a given task use `task.assignments(limit=None, marker=None, fields=None)`

```python
task_id = '1234'
assignments = client.task(task_id).assignments()
for assignment in assignments:
    # Do something
```

Get Information about Task Assignment
-------------------------------------

To retrieve information about a task assignment use, `task_assignment.get()`

```python
task_assignment_id = '2222'
assignment_info = client.task_assignment(task_assignment_id).get()
```

Update Task Assignment
----------------------

To update information about a task assignment use, `task_assignment.update_info()`

```python
from boxsdk.object.task_assignment import ResolutionState
task_assignment_id = '2222'
updated_task = {'resolution_state': ResolutionState.APPROVED}
updated_assignment = client.task_assignment(task_assignment_id).update_info(updated_task)
```

Delete Task Assignment
----------------------

To delete a task assignment use, `task_assignment.delete()`

```python
task_assignment_id = '2222'
client.task_assignment(task_assignment_id).delete()
```
