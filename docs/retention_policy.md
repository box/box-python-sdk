Retention Policies
==================

A retention policy blocks permanent deletion of content for a specified amount of time. Admins can create retention policies and then later assign them to specific folders or their entire enterprise.

- [Create Retention Policy](#create-retention-policy)
- [Get Retention Policy](#get-retention-policy)
- [Update Retention Policy](#update-retention-policy)
- [Get Retention Policies](#get-retention-policies)
- [Get Retention Policy Assignments](#get-retention-policy-assignments)
- [Create Retention Policy Assignment](#create-retention-policy-assignment)
- [Get Retention Policy Assignment](#get-retention-policy-assignment)

Create Retention Policy
-----------------------

You can call [`create_retention_policy(policy_name, disposition_action)`][create-indefinite-policy] to let you create a new indefinite retention policy.

```python
policy_name = 'Test Indefinite Policy Name'
disposition_action = 'remove_retention'
indefinite_retention_policy = client.create_retention_policy(policy_name, disposition_action)
```

Alternatively, if you want to create a finite retention policy, you can do so by calling [`create_retention_policy(policy_name, disposition_action, retention_length=5)`][create-finite-policy]

```python
policy_name = 'Test Finite Policy Name'
disposition_action = 'remove_retention'
retention_length = 5
finite_retention_policy = client.create_retention_policy(policy_name=policy_name, disposition_action=disposition_action, retention_length=retention_length)
```

Get Retention Policy
--------------------

Calling [`get()`][get-retention-policy] will return a retention policy object.

```python
policy_id = '1234'
retention_policy = client.retention_policy(policy_id)
policy_object - retention_policy.get()
```

Get Retention Policies
----------------------

Calling [`retention_policies()`][get-retention-policies] will return all retention policies for the enterprise.

```python
retention_policies = client.retention_policies()
first_policy = retention_policies.next()
```

Update Retention Policy
-----------------------

Calling [`update()`][update-retention-policy] will return the updated retention policy object.

```python
policy_id = '1234'
policy_update = {'policy_name': 'New Policy Name',}
retention_policy = client.retention_policy(policy_id).get()
updated_policy = retention_policy.update_info(policy_update)
```

Create Retention Policy Assignment
----------------------------------

To create a new retention policy assignment call [`assign(item)`][create-assignment] to assign the policy to a specific enterprise, 
folder, or metadata_template If assigining to an enterprise you will not have to provide the ID.

```python
policy_id = '1234'
item_to_assign = {'type': 'folder', 'id': '1111'}
retention_policy = client.retention_policy(policy_id)
policy_assignment = retention_policy.assign(item_to_assign)
```

Get Retention Policy Assignment
-------------------------------

Calling [`get()`][get-assignment] will return the retention policy assignment object.

```python
assignment_id = '1234'
assignment = client.retention_policy_assignment(assignment_id)
assignment_info = assignment.get()
```

Get Retention Policy Assignments
--------------------------------

Calling [`assigments()`][get-assignments] will return all retention policy assignments for the enterprise. It is possible to specify maximum number of items per single reponse with
[`assignments(limit=10)`][get-assignments-with-limit].

```python
policy_id = '1234'
assignments = client.retention_policy(policy_id).assignments(limit=10)
first_assignment = assignments.next()
```

Alternatively, you can also specify the `type` of assignment to retrieve with [`assignments(assignment_type='folder')`][get-assignments-for-type].

```python
policy_id = '1234'
assignments = client.retention_policy(policy_id).assignments(assignment_type='folder', limit=10)
first_assignment = assignments.next()
```