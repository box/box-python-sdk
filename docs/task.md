Tasks
=====

Tasks enable file-centric workflows in Box. User can create tasks on files and assign them to collaborators on Box.

Get a Task's Information
------------------------

To get a task object, first call [`client.task(task_id)`][task] to construct the appropriate [`Task`][task_class] object, and then calling [`task.get(fields=None)`][get] will return the [`Task`][task_class] object populated with data from the API, leaving the original object unmodified.

```python
task = client.task('12345').get()
print('Task id is {0} and the type is {1}'.format(task.id, task.type))
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.task
[task_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List Tasks on File
------------------

To retrieve all tasks on a file, call [`client.file(file_id)`][file] to create the appropriate [`File`][file_class] object. Then calling [`file.get_tasks(fields=None)`]['get_tasks'] will return a `BoxObjectCollection` that allows you to iterate over the [`Task`][task_class] objects in the collection.

```python
tasks = client.file('1111').get_tasks()
for task in tasks:
    print('Task id is {0} and the type is {1}'.format(task.id, task.type))
```

[file]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.file
[file_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File
[get_tasks]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_tasks()
[task_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task

Add Task to File
----------------

To create a single task for a single user on a single file, call [`client.file(file_id)`][file] to construct the appropriate [`File`][file_class] object. Calling [`file.create_task(message=None, due_at=None)`][create_task] will return a newly created [`Task`][task_class] object populated with data from the API, leaving the original object unmodified.

```python
message = 'Please review this'
due_at = "2014-04-03T11:09:43-07:00"
task = client.file('11111').create_task(message, due_at)
print('Task message is {0} and it is due at {1}'.format(task.message, task.due_at))
```

[file]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.task
[file_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File
[create_task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.create_Task
[task_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task

Update Task Info
----------------

To update a task object, first call [`client.task(task_id)`][task] to construct the appropriate task object, and then calling [`task.update_info(data)`][update_info] with a `dict` of properties to update on the task. This method returns a newly updated [`Task`][task_class] object, leaving the original object unmodified.

```python
task_update = {'message': 'New Message', 'due_at': '2014-04-03T11:09:43-10:00',}
updated_task = client.task('12345').update_info(task_update)
print('New task message is {1} and the new due time is {1}'.format{updated_task.message, updated_Task.due_at})
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.task
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info
[task_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task

Delete a Task
-------------

To delete a task, first call [`client.task(task_id)`][task] to construct the appropriate task object, and then call [`task.delete()`][delete]. This method returns `True` to indicate that the deleteion was successful.

```python
client.client.task('12345').delete()
print('The task was successfully delete!')
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.task
[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete


Assign a Task
--------------

To assign a task object, first call [`client.task(task_id)`][task] to construct the appropriate task object, then call [`client.user(user_id)`][user] to construct the appropriate user object you wish to assign the task to. Finally, calling [`task.assign(user)`][assign] will return an [`Assignment`][assignment_class] object, populated with data from the API.

```python
user = client.user('11111')
assignment = client.task('12345').assign(user)
print('Assignment id is {0} and is assigned to user {1}'.format(assignment.id, assignment.assigned_to.name))
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.task
[user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client/user
[assign]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task.assign
[assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task_assignment.TaskAssignment

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
