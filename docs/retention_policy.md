Retention Policies
==================

A retention policy blocks permanent deletion of content for a specified amount of time. Admins can create retention policies and then later assign them to specific folders or their entire enterprise.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Create Retention Policy](#create-retention-policy)
- [Get Retention Policy](#get-retention-policy)
- [Get Retention Policies](#get-retention-policies)
- [Update Retention Policy](#update-retention-policy)
- [Assign Retention Policy](#assign-retention-policy)
- [Get Retention Policy Assignment](#get-retention-policy-assignment)
- [Get Retention Policy Assignments](#get-retention-policy-assignments)
- [Get File Version Retentions](#get-file-version-retentions)
- [Get Information about a File Version Retention](#get-information-about-a-file-version-retention)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create Retention Policy
-----------------------

To create a retention policy object, call [`client.create_retention_policy(policy_name, disposition_action, retention_length, can_owner_extend_retention=None, are_owners_notified=None, custom_notification_recipients=None)`][create_retention_policy]. This will let you create a new indefinite [`Retention Policy`][retention_policy_class] object populated with data from the API.

```python
policy_name = 'Test Indefinite Policy Name'
disposition_action = 'remove_retention'
indefinite_retention_policy = client.create_retention_policy(policy_name, disposition_action, float('inf'))
print('Indefinite Retention Policy id is {0} and the policy name is {1}'.format(indefinite_retention_policy.id, indefinite_retention_policy.policy_name))
```

Alternatively, if you want to create a finite retention policy, you can do so by calling [`client.create_retention_policy(policy_name, disposition_action, retention_length=5)`][create_retention_policy]

```python
policy_name = 'Test Finite Policy Name'
disposition_action = 'remove_retention'
retention_length = 5
finite_retention_policy = client.create_retention_policy(policy_name=policy_name, disposition_action=disposition_action, retention_length=retention_length)
print('Finite Retention Policy is {0} and the policy name is {1}'.format(finite_retention_policy.id, finite_retention_policy.policy_name))
```

[create_retention_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.Client.create_retention_policy
[retention_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.RetentionPolicy

Get Retention Policy
--------------------

To get a retention policy object, first call [`client.retention_policy(policy_id)`][retention_policy] to construct the appropriate [`Retention Policy`][retention_policy_class] object, and then calling [`retention_policy.get(fields=None)`][get] will return the [`Retention Policy`][retention_policy_class] object populated with data from the API.

```python
retention_policy = client.retention_policy('12345').get()
print('Retention Policy id is {0} and the name is {1}'.format(retention_policy.id, retention_policy.policy_name))
```

[retention_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.retention_policy
[retention_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.retention_policy
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Get Retention Policies
----------------------

To retrieve all retention policies for an enterprise, call [`client.get_retention_policies`][get_retention_policies]. This method returns a `BoxObjectCollection` that allows you to iterate over the [`Retention Policy`][retention_policy_class] objects in the collection.

```python
retention_policies = client.get_retention_policies()
for policy in retention_policies:
    print('The policy id is {0} and the name is {1}'.format(policy.id, policy.policy_name))
```

[get_retention_policies]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.get_retention_policies
[retention_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.RetentionPolicy

Update Retention Policy
-----------------------

To update a retention policy object, first call [`client.retention_policy(policy_id)`][retention_policy] to construct the appropriate [`Retention Policy`][retention_policy_class] object, and then calling [`retention_policy.update_info(data)`][update_info] with a `dict` of properties to update on the retention policy. This method returns a newly updates [`Retention Policy`][retention_policy_class] object, leaving the original object unmodified.

```python
policy_update = {'policy_name': 'New Policy Name',}
updated_retention_policy = client.retention_policy('12345').update_info(policy_update)
print('Retention Policy id is {0} and the new policy name is {1}'.format(updated_retention_policy.id, updated_retention_policy.policy_name))
```

[retention_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.retention_policy
[retention_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.retention_policy
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Assign Retention Policy
-----------------------

To assign a retention policy, first call [`client.retention_policy(policy_id)`][retention_policy] to construct the appropriate [`Retention Policy`][retention_policy_class] object. Then calling [`client.folder('56781')`][folder] to construct the folder you wish to assign a retention policy to. Finally calling [`retention_policy.assign(folder)`][assign] will create a new [`Retention Policy Assignment`][retention_policy_assignment_class] object populated with data from the API.

```python
folder = client.folder('1111')
policy_assignment = client.retention_policy('12345').assign(folder)
```

[folder]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.folder
[retention_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.retention_policy
[retention_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.RetentionPolicy
[retention_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy_assignment.RetentionPolicyAssignment
[assign]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.RetentionPolicy.assign

Get Retention Policy Assignment
-------------------------------

To get a retention policy object, first call [`client.retention_policy_assignment(assignment_id)`][retention_policy_assignment] to construct the appropriate [`Retention Policy Assignment`][retention_policy_assignment_class] object, and then calling [`retention_policy_assignment.get(fields=None)`][get] will return the [`Retention Policy Assignment`][retention_policy_assignment_class] object populated with data from the API.

```python
assignment = client.retention_policy_assignment('12345').get()
print('Assignment id is {0} and it is assigned by {1}'.format(assignment.id, assignment.assigned_by.name))
```

[retention_policy_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.retention_policy_assignment
[retention_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy_assignment.RetentionPolicyAssignment
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Get Retention Policy Assignments
--------------------------------

To retrieve all retention policy assignments for an enterprise, first call [`client.retention_policy(policy_id)`][retention_policy] to construct the appropriate [`Retention Policy`][retention_policy_class] object. Then call [`retention_policy.assignments(assignment_type=None, limit=None, marker=None, fields=None)`][get_assignments] will return a `BoxObjectCollection` that allows you to iterate over the [`Retention Policy Assignment`][retention_policy_assignment_class] objects in the collection.

```python
assignments = client.retention_policy('12345').assignments(limit=10)
for assignment in assignments:
    print('Assignment id is {0} and it is assigned by {1}'.format(assignment.id, assignment.assigned_by.name))
```

Alternatively, you can also specify the `type` of assignment to retrieve with [`retention_policy.assignments(assignment_type='folder')`][get_assignments].

```python
assignments = client.retention_policy('12345').assignments(assignment_type='folder', limit=10)
for assignment in assignments:
    print('Assignment id is {0} and it is assigned by {1}'.format(assignment.id, assignment.assigned_by.name))
```

[retention_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.retention_policy
[retention_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.RetentionPolicy
[retention_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy_assignment.RetentionPolicyAssignment
[get_assignments]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.retention_policy.assignments

Get File Version Retentions
---------------------------

To retrieve all file version retentions, call [`client.get_file_version_retentions(target_file=None, file_version=None, policy_id=None, disposition_action=None, disposition_before=None, disposition_after=None, limit=None, marker=None, fields=None)`][get_file_version_retentions]. This method will return a `BoxObjectCollection` that allows you to iterate over the [`File Version Retention`][file_version_retention_class] objects in the collection.

```python
retentions = client.get_file_version_retentions()
for retention in retentions:
    print('The file version retention id is {0} and the data time applied at is {1}'.format(retention.id, retention.applied_at))
```

[get_file_version_retentions]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.get_file_version_retentions
[file_version_rention_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_version_retention.FileVersionRetention


Get Information about a File Version Retention
----------------------------------------------

To get a file version retention object, first call [`client.file_version_retention(retention_id)`][file_version_retention] to construct the appropriate [`File Version Retention`][file_version_retention_class] object, and then calling [`file_version_retention.get(fields=None)`][get] will return the [`File Veresion Retention`][file_version_retention] object populated with data from the API.

```python
retention_info = client.file_version_retention('12345').get()
```

[file_version_retention]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.file_version_retention
[file_version_retention_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_version_retention.FileVersionRetention
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get
