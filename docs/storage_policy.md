Storage Policy 
==============

Allows the enterprise admin to manage the Storage Policies for users in their
enterprise. Used for an enterprise to decide storage location for users based on
where they work/reside. 


Get Storage Policy
------------------

Calling `storage_policy.get(fields=None)` will return the storage policy object.

```python
storage_policy_id = '1234'
storage_policy = client.storage_policy(storage_policy_id).get()
```

List Available Storage Policies
-------------------------------

Calling `client.get_storage_policies()` will return an iterable that will page through all of the storage policies. It is possible to specify maxiumum number of items per response and fields to retrieve by caling `client.get_storage_policies(limit=None, fields=None)`.

```python
storage_policies = client.get_storage_policies(limit=100)
for storage_policy in storage_policies:
    # Do something
```

Create Storage Policy Assignment
--------------------------------

To create new storage policy assignment call `storage_policy.create_assignment(user)`.

```python
storage_policy_id = '5678'
user = client.user('1234')
storage_policy_assignment = client.storage_policy(storage_policy_id).create_assignment(user)
```

Note: This method only works if the user does not already have an assignment. If the current state of the user is not known, use the `storage_policy.assign(user)` method instead.

Assign a Storage Policy to a User
---------------------------------

To assign a storage policy to a user, call the `storage_policy.assign(user)` method with the user to assign the storage policy to.

```python
user = client.user('1234')
storage_policy_assignment = client.storage_policy('12345').assign(user)
```

Update Existing Assignment
--------------------------

Updating a storage policy assignment is done by calling `storage_policy.update_info(update_item)`.

```python
updated_storage_policy = {'storage_policy': {'type': 'storage_policy', 'id': '1234'}}
updated_assignment = client.storage_policy_assignment('ZW50ZXJwcmldfgeV82MDMwMDQ=').update_info(updated_storage_policy)
```

Get Assignment
--------------

Calling `storage_policy_assignment.get(fields=None)` will return a storage policy assignment object containing information about the assignment.

```python
assignment_id = '1234'
storage_policy_assignment = client.storage_policy_assignment(assignment_id).get()
```

Get Assignment for User
-------------------------

Calling `user.get_storage_policy_assignment()` will return the storage policy assigned to the specified user.

```python
user_id = '1111'
assignment_info = client.user(user_id).get_storage_policy_assignment()
```

Delete Assignment
-----------------

Calling `storage_policy_assignment.delete()` will remove the storage policy assignment from the user.

```python
assignment_id = '1234'
client.storage_policy_assignment(assignment_id).delete()
```
