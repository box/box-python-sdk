Legal Holds Policy
==================

Legal Hold Policy information describes the basic characteristics of the Policy,
such as name, description, and filter dates.


Get Legal Hold Policy Information
---------------------------------

To retrieve information about a legal hold policy, use `legal_hold_policy.get()`.

```python
policy_id = '1234'
policy_info = client.legal_hold_policy(policy_id).get()
```

List Legal Hold Policies
------------------------

To retrieve an interable of legal hold policies in the enterprise, you can call `client.legal_hold_policies(policy_name=None, limit=None, marker=None, fields=None)`.

```python
policies = client.legal_hold_policies()
for policy in policies:
    # Do something
```

You can also specify a name filter for the policies you wish to retrieve by using

```python
policies = clinet.legal_hold_policies(policy_name='Test Policy')
for policy in policies:
    # Do something
```

Create New Legal Hold Policy
----------------------------

To create a new legal hold policy, use `client.create_legal_hold_policy(policy_name, description=None, filter_starting_at=None, filter_ending_at=None, is_ongoing=None)`.

```python
new_policy = client.create_legal_hold_policy('New Policy')
```

Update Legal Hold Policy
------------------------

To update an existing legal hold policy, use `legal_hold_policy.update_info()`

```python
policy_id = '1234'
policy_update = {'description': 'New Description', 'release_notes': 'Example Notes'}
updated_policy = client.legal_hold_policy(policy_id).update_info(policy_update)
```

Delete Legal Hold Policy
------------------------

To delete a legal hold policy, use `legal_hold_policy.delete()`

```python
policy_id = '1234'
client.legal_hold_policy(policy_id).delete()
```

Assign Legal Hold Policy
------------------------

To assign a legal hold policy, use `legal_hold_policy.assign(assignee)`. You can assign a legal hold policy to a `file_version`, `file`, `user`, or `folder`.

```python
folder_id = '1234'
policy_id = '5678'
folder_to_assign = client.folder(folder_id)
assignment = client.legal_hold_policy(policy_id).assign(folder_to_assign)
```

List Legal Hold Policy Assignments
----------------------------------

To retrieve an iterable of legal hold policy assignments, use `legal_hold_policy.get_assignments(assign_to_type=None, assign_to_id=None, limit=None, marker=None, fields=None)`

```python
assignments = client.legal_hold_policy('1234').get_assignments()
for assignment in assignments:
    # Do something
```

To filter by the assignee `type` and `id` you can use pass in the `assign_to_type` and `assign_to_id` filter.

```python
folder_id = '1111'
assignments = client.legal_hold_policy('1234').get_assignments('folder', folder_id)
for assignment in assignments:
    # Do something
```

Get Legal Hold Assignment Information
--------------------------

To retrieve information about the legal hold policy assignment, use `legal_hold_policy_assignment.get()`

```python
assignment_id = '1111'
assignment_info = client.legal_hold_policy_assignment(assignment_id).get()
```

Delete Legal Hold Assignment
----------------------------

To delete an existing legal hold policy assignment, use `legal_hold__policy_assignment.delete()`

```python
assignment_id = '1111'
client.legal_hold_policy_assignment.delete()
```
