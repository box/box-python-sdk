Storage Policy 
==============

Allows the enterprise admin to manage the Storage Policies for users in their
enterprise. Used for an enterprise to decide storage location for users based on
where they work/reside. 


Get Storage Policy
------------------

Calling `storage_policy.get(storage_policy_id)` will return the storage policy object.

```python
storage_policy_id = '1234'
storage_policy = client.storage_policy(storage_policy_id).get()
```

List Available Storage Policies
-------------------------------

Calling `client.storage_policies()` will return an iterable that will page through all of the storage policies. It is possible to specify maxiumum number of items per response and fields to retrieve by caling `client.storage_policies(limit=None, fields=None)`.

```python
storage_policies = client.storage_policies(limit=100)
for storage_policy in storage_policies:
    # Do something
```

Assign Storage Policy
---------------------

To create new storage policy assignment call `storage_policy.assign(item)`.

```python
storage_policy_id = '5678'
user = client.user('1234')
storage_policy_assignment = client.storage_policy(storage_policyid).assign(user)
```

Update Existing Assignment
--------------------------

Updating a storage policy assignment is done by calling `storage_policy.update_info(update_item)`.

```python
storage_policy_assignment_id = '1234'
new_storage_policy_id = '5678'
updated_item = {'type': 'storage_policy', 'id': new_storage_policy_id}
updated_storage_policy_assignment = client.storage_policy_assignment(storage_policy_assignment).update_info(updated_item)
```

Get Assignment
--------------

Calling `storage_policy_assignment.get()` will return a storage policy assignment object containing information about the assignment.

```python
assignment_id = '1234'
storage_policy_assignment = client.storage_policy_assignment(assignment_id).get()
```

Get Assignment for Target
-------------------------

Calling `client.storage_policy_assignments(resolved_for_type, resolved_for_id)` will return a storage policy assignment object

```python
resolved_for_type = 'user'
resolved_for_id = '1234'
assignment_info = client.storage_policy_assignments(resolved_for_type, resolved_for_id)
```

Delete Assignment
-----------------

Calling `storage_policy_assignment.delete()` will remove the storage policy assignment from the user.

```python
assignment_id = '1234'
policy_assignment = client.storage_policy_assignment(assignment_id).delete()
```