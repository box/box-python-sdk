Storage Policy 
==============

Allows the enterprise admin to manage the Storage Policies for users in their
enterprise. Used for an enterprise to decide storage location for users based on
where they work/reside. 

* [Get Storage Policy](#get-storage-policy) 
* [Get List of Storage Policies](#get-list-of-storage-policies)
* [Create New Assignment](#create-new-assignment)
* [Get Assignment](#get-assignment)
* [Get Assignment For Target](#get-assignment-for-target)
* [Update Existing Assignment](#update-existing-assignment)
* [Assign Storage Policy](#assign-storage-policy)
* [Delete Assignment](#delete-assignment)

Get Storage Policy
------------------

Calling ['get('storage_policy_id')'][get-info] will return the storage policy object.

```python
storage_policy_id = '1234'
storage_policy = client.storage_policy(storage_policy_id)
storage_policy_info = storage_policy.get()
```

Get List of Storage Policies
----------------------------

Calling ['storage_policies()'][get-all] will return an iterable that will page through all of the storage policies. It is possible to specify maxiumum number of items per response and fields to retrieve by caling ['storage_policies(limit=number_of_entries, fields=fields_to_retrieve)'][get-all-with-params].

```python
storage_policies = client.storage_policies(limit=100)
```

Assign Storage Policy
---------------------

To create new storage policy assignment call ['assign(item)'][assign].

```python
storage_policy_id = '5678'
item = {'type': 'user', 'id': '1234'}
storage_policy = client.storage_policy(storage_policyid)
storage_policy_assignment = storage_policy.assign(item)
```

Update Existing Assignment
--------------------------

Updating a storage policy assignment is done by calling ['update_info(update_item)'][update-info].

```python
storage_policy_assignment_id = '1234'
new_storage_policy_id = '5678'
updated_item = {'type': 'storage_policy', 'id': new_storage_policy_id}
storage_policy_assignment = client.storage_policy_assignment(storage_policy_assignment)
updated_assignment_info = storage_policy_assignment.update_info(updated_item)
```

Get Assignment
--------------

Calling ['get()'][get-assignment-info] will return a storage policy assignment object containing information about the assignment.

```python
assignment_id = '1234'
storage_policy_assignment = client.storage_policy_assignment(assignment_id)
assignment_info = storage_policy_assignment.get()
```

Get Assignment for Target
-------------------------

Calling ['storage_policy_assignments(resolved_for_type, resolved_for_id)'][get-assignment-for-target] will return a storage policy assignment object

```python
resolved_for_type = 'user'
resolved_for_id = '1234'
assignment_info = client.storage_policy_assignments(resolved_for_type, resolved_for_id)
```

Delete Assignment
-----------------

Calling [`delete()`][delete] will remove the storage policy assignment from the user.

```python
assignment_id = '1234'
policy_assignment = client.storage_policy_assignment(assignment_id)
policy_assignment.delete()
```