Tasks
=====

Task objects represent a user-created task on a file.


Get a Task's Information
------------------------

Calling `task.get(fields=None, headers=None)` will return information about the specified task.

```python
task_info = client.task('1234').get()
```

List Tasks on File
------------------

To retrieve all tasks for a given file use, `file.get_tasks(fields=None)`.

```python
tasks = client.file('1111').get_tasks()
for task in tasks:
    # Do something
```

Add Task to File
----------------

To create a single task for a single user on a single file use, `file.create_task(message=None, due_at=None)`

```python
message = 'Please review this'
due_at = "2014-04-03T11:09:43-07:00"
task = client.file('11111').create_task(message, due_at)
```

Update Task Info
----------------

To update the task information use, `task.update_info(data)`

```python
task_update = {'message': 'New Message', 'due_at': '2014-04-03T11:09:43-10:00',}
updated_task = client.task('1234').update_info(task_update)
```

Delete a Task
-------------

To delete a task, use `task.delete()`

```python
client.client.task('1234').delete()
```

Assign a Task
--------------

To assign a task to a user on a file, use `task.assign(assignee)`

```python
user = client.user('1111')
assignment = client.task('1234').assign(user)
```

Assign a Task with User Login
-----------------------------

To assign a task to a user on a file, use `task.assign_with_login(assignee_login)`

```python
assignment = client.task('1234').assign_with_login('test_user@example.com')
```

List Task Assignments
---------------------

To retrieve all task assignments for a given task use `task.get_assignments(fields=None)`

```python
assignments = client.task('1234').get_assignments()
for assignment in assignments:
    # Do something
```

Get Information about Task Assignment
-------------------------------------

To retrieve information about a task assignment use, `task_assignment.get(fields=None, headers=None)`

```python
task_assignment_id = '2222'
assignment_info = client.task_assignment(task_assignment_id).get()
```

Update Task Assignment
----------------------

To update information about a task assignment use, `task_assignment.update_info(data)`

```python
from boxsdk.object.task_assignment import ResolutionState
updated_task = {'resolution_state': ResolutionState.APPROVED}
updated_assignment = client.task_assignment('5678').update_info(updated_task)
```

Delete Task Assignment
----------------------

To delete a task assignment use, `task_assignment.delete()`

```python
client.task_assignment('2222').delete()
```
