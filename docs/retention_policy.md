Retention Policies
==================

A retention policy blocks permanent deletion of content for a specified amount of time. Admins can create retention policies and then later assign them to specific folders or their entire enterprise.

Create Retention Policy
-----------------------

You can call `client.create_retention_policy(policy_name, disposition_action, can_owner_extend_retention=None, are_owners_notified=None, retention_length=None, custom_notification_recipients=None)` to let you create a new indefinite retention policy.

```python
policy_name = 'Test Indefinite Policy Name'
disposition_action = 'remove_retention'
indefinite_retention_policy = client.create_retention_policy(policy_name, disposition_action)
```

Alternatively, if you want to create a finite retention policy, you can do so by calling `client.create_retention_policy(policy_name, disposition_action, retention_length=5)`

```python
policy_name = 'Test Finite Policy Name'
disposition_action = 'remove_retention'
retention_length = 5
finite_retention_policy = client.create_retention_policy(policy_name=policy_name, disposition_action=disposition_action, retention_length=retention_length)
```

Get Retention Policy
--------------------

Calling `client.get()` will return a retention policy object.

```python
policy_id = '1234'
retention_policy = client.retention_policy(policy_id).get()
```

Get Retention Policies
----------------------

Calling `client.get_retention_policies()` will return all retention policies for the enterprise.

```python
retention_policies = client.get_retention_policies()
for policy in retention_policies:
    # Do something
```

Update Retention Policy
-----------------------

Calling `retention_policy.update_info()` will return the updated retention policy object.

```python
policy_id = '1234'
policy_update = {'policy_name': 'New Policy Name',}
updated_retention_policy = client.retention_policy(policy_id).update_info(policy_update)
```

Assign Retention Policy
-----------------------

To create a new retention policy assignment call `retention_policy.assign(item)` to assign the policy to a specific enterprise, 
folder, or metadata_template If assigining to an enterprise you will not have to provide the ID.

```python
policy_id = '1234'
item_to_assign = {'type': 'folder', 'id': '1111'}
retention_policy = client.retention_policy(policy_id)
policy_assignment = retention_policy.assign(item_to_assign)
```

Get Retention Policy Assignment
-------------------------------

Calling `retention_polict_assignment.get()` will return the retention policy assignment object.

```python
assignment_id = '1234'
assignment = client.retention_policy_assignment(assignment_id).get()
```

Get Retention Policy Assignments
--------------------------------

Calling `retention_policy.assigments()` will return all retention policy assignments for the enterprise. It is possible to specify maximum number of items per single reponse with
`retention_policy.assignments(limit=10)`.

```python
policy_id = '1234'
assignments = client.retention_policy(policy_id).assignments(limit=10)
for assignment in assignments:
    # Do something
```

Alternatively, you can also specify the `type` of assignment to retrieve with `retention_policy.assignments(assignment_type='folder')`.

```python
policy_id = '1234'
assignments = client.retention_policy(policy_id).assignments(assignment_type='folder', limit=10)
for assignment in assignments:
    # Do something
```

Get File Version Retentions
---------------------------

Calling `client.get_file_version_retentions(file_id=None, file_version_id=None, policy_id=None, disposition_action=None, disposition_before=None, disposition_after=None, limit=None, marker=None, fields=None)` will return an iterable of file version retentions for the enterprise.

```python
retentions = client.get_file_version_retentions()
for retention in retentions:
    # Do something
```

Get Information about a File Version Retention
----------------------------------------------

Calling `file_version_retention.get()` will return information about the specific file version retention.

```python
retention_info = client.file_version_retention('1234').get()
```