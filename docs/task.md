Tasks
=====

Tasks enable file-centric workflows in Box. User can create tasks on files and assign them to collaborators on Box.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get a Task's Information](#get-a-tasks-information)
- [List Tasks on File](#list-tasks-on-file)
- [Add Task to File](#add-task-to-file)
- [Update Task Info](#update-task-info)
- [Delete a Task](#delete-a-task)
- [Assign a Task](#assign-a-task)
- [Assign a Task with User Login](#assign-a-task-with-user-login)
- [List Task Assignments](#list-task-assignments)
- [Get Information about Task Assignment](#get-information-about-task-assignment)
- [Update Task Assignment](#update-task-assignment)
- [Delete Task Assignment](#delete-task-assignment)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get a Task's Information
------------------------

To get a task object, first call [`client.task(task_id)`][task] to construct the appropriate [`Task`][task_class] 
object, and then calling [`task.get(fields=None)`][get] will return the [`Task`][task_class] object populated with data 
from the API, leaving the original object unmodified.

```python
task = client.task(task_id='12345').get()
print('Task ID is {0} and the type is {1}'.format(task.id, task.type))
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.task
[task_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List Tasks on File
------------------

To retrieve all tasks on a file, call [`file.get_tasks(fields=None)`]['get_tasks'] will return a `BoxObjectCollection` 
that allows you to iterate over the [`Task`][task_class] objects in the collection.

```python
tasks = client.file(file_id='11111').get_tasks()
for task in tasks:
    print('Task ID is {0} and the type is {1}'.format(task.id, task.type))
```

[get_tasks]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_tasks()
[task_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task

Add Task to File
----------------

To create a single task for a single user on a single file, call [`file.create_task(message=None, due_at=None)`][create_task] 
will return a newly created [`Task`][task_class] object populated with data from the API.

```python
message = 'Please review this'
due_at = "2014-04-03T11:09:43-07:00"
task = client.file(file_id='11111').create_task(message, due_at)
print('Task message is {0} and it is due at {1}'.format(task.message, task.due_at))
```

[create_task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.create_Task

Update Task Info
----------------

To update a task object, first call [`task.update_info(data)`][update_info] with a `dict` of properties to update on the 
task. This method returns a newly updated [`Task`][task_class] object, leaving the original object unmodified.

```python
task_update = {'message': 'New Message', 'due_at': '2014-04-03T11:09:43-10:00',}
updated_task = client.task(task_id='12345').update_info(task_update)
print('New task message is {1} and the new due time is {1}'.format{updated_task.message, updated_Task.due_at})
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info
[task_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task

Delete a Task
-------------

To delete a task, first call [`client.task(task_id)`][task] to construct the appropriate task object, and then call 
[`task.delete()`][delete]. This method returns `True` to indicate that the deleteion was successful.

```python
client.client.task('12345').delete()
print('The task was successfully delete!')
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.task
[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete


Assign a Task
--------------

To assign a task object, first call [`client.task(task_id)`][task] to construct the appropriate task object, then call 
[`task.assign(user)`][assign] will return an [`Task Assignment`][assignment_class] object, populated with data 
from the API.

```python
user = client.user(user_id='11111')
assignment = client.task(task_id='12345').assign(user)
print('Assignment ID is {0} and is assigned to user {1}'.format(assignment.id, assignment.assigned_to.name))
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client..html#boxsdk.client.client.Client.task
[assign]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task.assign
[assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task_assignment.TaskAssignment

Assign a Task with User Login
-----------------------------

To assign a task object with a user login, first call [`task.assign_with_login(login)`][assign_with_login] with a 
`unicode` value for user login. This method will return a [`TaskAssignment`][assignment_class] object, populated with 
data from the API.

```python
assignment = client.task(task_id='12345').assign_with_login('test_user@example.com')
print('Assignment ID is {0} and the assignee is {1}'.format(assignment.id, assignment.assigned_to.login))
```

[assign_with_login]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task_assignment.assign_with_login
[assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task_assignment.TaskAssignment

List Task Assignments
---------------------

To retrieve all assignments for an enterprise, first call [`client.task(task_id)`][task] to construct the appropriate 
task object. Then call ['task.get_assignments(fields=None)'][get_assignments]. This method returns a 
`BoxObjectCollection` that allows you to iterate over the ['TaskAssignment'][assignment_class] objects in the 
collection.

```python
assignments = client.task(task_id='12345').get_assignments()
for assignment in assignments:
    print('Assignment ID is {0} and the assignee is {1}'.format(assignment.id, assignment.assigned_to.login))
```

[task]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.task
[get_assignments]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task.Task.get_assignments

Get Information about Task Assignment
-------------------------------------

To get a task assignment object, first call [`client.task_assignment(assignment_id)`][assignment] to construct the 
appropriate [`TaskAssignment`][assignment_class] object, and then calling ['task_assignment.get(fields=None)'][get] 
will return the [`TaskAssignment`][task_assignment] object populated with data from the API.

```python
assignment= client.task_assignment('12345').get()
print('Assignment ID is {0} and assignment type is {1}'.format(assignment.id, assignment.type))
```

[assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.task_assignment
[assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task_assignment.TaskAssignment
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Update Task Assignment
----------------------

To update a task assignment object, call [`assignment.update_info(data)`][update_info] 
with a `dict` of properties to update on a task assignment. This method returns a newly update 
[`TaskAssignment`][assignment_class] object, leaving the original object unmodified.

```python
from boxsdk.object.task_assignment import ResolutionState
updated_task = {'resolution_state': ResolutionState.APPROVED}
updated_assignment = client.task_assignment(assignment_id='12345').update_info(updated_task)
print('Assignment ID is {0} and resolution state is {1}'.format(updated_assignment.id, updated_assignment.resolution_state))
```

[assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.task_assignment.TaskAssignment
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Delete Task Assignment
----------------------

To delete a task assignment, call [`task_assignment.delete()`][delete]. This method returns `True` to indicate that the 
deletion was successful.

```python
client.task_assignment(assignment_id='12345').delete()
print('The task assignment was successfully delete!')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete
