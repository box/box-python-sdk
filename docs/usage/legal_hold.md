Legal Hold Policies
===================


A legal hold policy blocks permanent deletion of content during ongoing litigation. Admins can create legal hold
policies and then later assign them to specific folders, files, or users.

Legal Hold Policy information describes the basic characteristics of the Policy, such as name, description, and filter
dates. It is important to note that the legal hold object contains no information about what this policy applies to.

If an order of discovery is received or the customer is part of an ongoing litigation, a legal hold policy can be
created to keep track of everything that needs to be held. The actual holding is done via Legal Hold Assignments.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get Information About a Legal Hold Policy](#get-information-about-a-legal-hold-policy)
- [List Legal Hold Policies](#list-legal-hold-policies)
- [Create New Legal Hold Policy](#create-new-legal-hold-policy)
- [Update Legal Hold Policy](#update-legal-hold-policy)
- [Delete Legal Hold Policy](#delete-legal-hold-policy)
- [Assign Legal Hold Policy](#assign-legal-hold-policy)
- [List Legal Hold Policy Assignments](#list-legal-hold-policy-assignments)
- [Get Information About a Legal Hold Assignment](#get-information-about-a-legal-hold-assignment)
- [Delete Legal Hold Assignment](#delete-legal-hold-assignment)
- [List File Version Legal Holds](#list-file-version-legal-holds)
- [Get Information about a File Version Legal Hold](#get-information-about-a-file-version-legal-hold)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Information About a Legal Hold Policy
-----------------------------------------

To retrieve information about a legal hold policy, first call [`client.legal_hold_policy(policy_id)`][legal_hold_policy]
to initialize the [`LegalHoldPolicy`][policy_class] and then call [`legal_hold_policy.get(*, fields=None, headers=None, **kwargs)`][get] to
retrieve data from the API.  This method returns a new [`LegalHoldPolicy`][policy_class] object with fields populated by
data form the API, leaving the original object unmodified.

<!-- sample get_legal_hold_policies_id -->
```python
legal_hold_policy = client.legal_hold_policy(policy_id='12345').get()
print(f'The "{legal_hold_policy.policy_name}" policy is {legal_hold_policy.status}')
```

[legal_hold_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.legal_hold_policy
[policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.legal_hold_policy.LegalHoldPolicy
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List Legal Hold Policies
------------------------

To get the legal hold policies available in the enterprise, call
[`client.get_legal_hold_policies(policy_name=None, limit=None, marker=None, fields=None)`][get_legal_hold_policies].
You can optionally pass a `policy_name` value to filter the results to include only policies that are a case-insensitive
prefix match by name.  This method returns a `BoxObjectCollection` that allows you to iterate over the
[`LegalHoldPolicy`][policy_class] objects in the collection.

<!-- sample get_legal_hold_policies -->
```python
policies = client.get_legal_hold_policies()
for policy in policies:
    print(f'Legal Hold Policy "{policy.name}" has ID {policy.id}')
```

[get_legal_hold_policies]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_legal_hold_policies

Create New Legal Hold Policy
----------------------------

To create a new legal hold policy, call
[`client.create_legal_hold_policy(policy_name, description=None, filter_starting_at=None, filter_ending_at=None, is_ongoing=None)`][create_legal_hold_policy] with the name for the policy.  You can optionally include a human-readable `description`, as
well as parameters describing which time period the policy applies to.  You must specify either `filter_starting_at`
and `filter_ending_at` dates, or `is_ongoing=True`.  This method returns a new [`LegalHoldPolicy`][policy_class] object
representing the created policy.

<!-- sample post_legal_hold_policies -->
```python
new_policy = client.create_legal_hold_policy('New Policy', is_ongoing=True)
print(f'Created legal hold policy with ID {new_policy.id}')
```

[create_legal_hold_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_legal_hold_policy

Update Legal Hold Policy
------------------------

To update an existing legal hold policy, call [`legal_hold_policy.update_info(data=policy_update)`][update_info] with
a `dict` of properties to update on the policy. This method returns a new [`LegalHoldPolicy`][policy_class] object
with the updates applied, leaving the original object unmodified.

<!-- sample put_legal_hold_policies_id -->
```python
policy_update = {'description': 'New Description', 'release_notes': 'Example Notes'}
updated_policy = client.legal_hold_policy(policy_id='12345').update_info(data=policy_update)
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Delete Legal Hold Policy
------------------------

To delete a legal hold policy, call [`legal_hold_policy.delete()`][delete].  This method returns `True` to indicate that
the deletion request was successful.

> __Note:__ This is an asynchronous process - the policy assignment may not be fully deleted yet when the
> response comes back.

<!-- sample delete_legal_hold_policies_id -->
```python
client.legal_hold_policy(policy_id='12345').delete()
print('Legal hold policy was deleted!')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete

Assign Legal Hold Policy
------------------------

To assign a legal hold policy, call [`legal_hold_policy.assign(assignee)`][assign].  You can assign a legal hold policy
to a [`Folder`][folder_class], [`File`][file_class], [`FileVersion`][file_version_class], or [`User`][user_class].
This will cause the associated items to be held and unable to be deleted.

<!-- sample post_legal_hold_policy_assignments -->
```python
folder_to_assign = client.folder(folder_id='22222')
assignment = client.legal_hold_policy(policy_id'12345').assign(folder_to_assign)
print(f'Applied policy "{assignment.legal_hold_policy.policy_name}" to {assignment.assigned_to.type} {assignment.assigned_to.id}')
```

[assign]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.legal_hold_policy.LegalHoldPolicy.assign
[folder_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder
[file_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File
[file_version_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_version.FileVersion
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User

List Legal Hold Policy Assignments
----------------------------------

To get the assignments for a specific legal hold policy, call
[`legal_hold_policy.get_assignments(assign_to_type=None, assign_to_id=None, limit=None, marker=None, fields=None)`][get_assignments].
This method returns a `BoxObjectCollection` that allows you to iterate over the
[`LegalHoldPolicyAssignment`][assignment_class] objects in the collection.

<!-- sample get_legal_hold_policy_assignments -->
```python
assignments = client.legal_hold_policy(policy_id='12345').get_assignments()
for assignment in assignments:
    print(f'Found policy assignment with ID {assignment.id}')
```

To filter by the assignee `type` and/or `id` you can use pass in the `assign_to_type` and `assign_to_id` filter.

```python
folder_id = '1111'
assignments = client.legal_hold_policy('1234').get_assignments('folder', folder_id)
for assignment in assignments:
    print(f'Found policy assignment with ID {assignment.id}')
```

[get_assignments]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.legal_hold_policy.LegalHoldPolicy.get_assignments
[assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.legal_hold_policy_assignment.LegalHoldPolicyAssignments

Get Information About a Legal Hold Assignment
---------------------------------------------

To retrieve information about a legal hold policy assignment, first call
[`client.legal_hold_policy_assignment(policy_assignment_id)`][legal_hold_policy_assignment] to initialize the
[`LegalHoldPolicyAssignment`][assignment_class] and then call [`legal_hold_policy_assignment.get(*, fields=None, headers=None, **kwargs)`][get] to
retrieve data about the assignment from the API.  This method returns a new
[`LegalHoldPolicyAssignment`][assignment_class] with fields populated by data from the API, leaving the original object
unmodified.

<!-- sample get_legal_hold_policy_assignments_id -->
```python
assignment_id = '98765'
assignment = client.legal_hold_policy_assignment(assignment_id).get()
print(f'Policy {assignment.legal_hold_policy.id} is assigned to {assignment.assigned_to.type} {assignment.assigned_to.id}')
```

[legal_hold_policy_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.legal_hold_policy_assignment

Delete Legal Hold Assignment
----------------------------

To delete an existing legal hold policy assignment, call [`legal_hold_policy_assignment.delete()`][delete].  This method
returns `True` to indicate that the deletion request was successful.

> __Note:__ This is an asynchronous process - the policy assignment may not be fully deleted yet when the
> response comes back.

<!-- sample delete_legal_hold_policy_assignments_id -->
```python
assignment_id = '1111'
client.legal_hold_policy_assignment(assignment_id).delete()
```

List File Version Legal Holds
-----------------------------

To get the actual hold records associated with a policy, call
[`legal_hold_policy.get_file_version_legal_holds()`][get_file_version_legal_holds].  This method returns a
`BoxObjectCollection` that allows you to iterate over the [`LegalHold`][hold_class] objects in the
collection.

<!-- sample get_file_version_legal_holds -->
```python
legal_holds = client.legal_hold_policy(policy_id='12345').get_file_version_legal_holds()
for legal_hold in legal_holds:
    print(f'Got file version legal hold with ID {legal_hold.id}')
```

[get_file_version_legal_holds]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.legal_hold_policy.LegalHoldPolicy.get_file_version_legal_holds
[hold_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.legal_hold.LegalHold

Get Information about a File Version Legal Hold
-----------------------------------------------

To retrieve information about a file version legal hold, call [`legal_hold.get(*, fields=None, headers=None, **kwargs)`][get].  This method
returns a new [`LegalHold`][hold_class] with fields populated by data from the API, leaving the original object
unmodified.

<!-- sample get_file_version_legal_holds_id -->
```python
file_version_legal_hold_id = '55555'
legal_hold = client.legal_hold(file_version_legal_hold_id).get()
print(f'Version {legal_hold.file_version.id} of file {legal_hold.file.id} is held by {len(legal_hold.legal_hold_policy_assignments)} assignment(s)')
```
