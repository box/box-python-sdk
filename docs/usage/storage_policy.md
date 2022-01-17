Storage Policies
================

Allows the enterprise admin to manage the Storage Policies for users in their
enterprise. Used for an enterprise to decide storage location for users based on
where they work/reside. 

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get Storage Policy](#get-storage-policy)
- [List Available Storage Policies](#list-available-storage-policies)
- [Assign a Storage Policy to a User](#assign-a-storage-policy-to-a-user)
- [Get Assignment Information about a Storage Policy Assignment](#get-assignment-information-about-a-storage-policy-assignment)
- [Get Assignment for User](#get-assignment-for-user)
- [Delete Assignment](#delete-assignment)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Storage Policy
------------------

To get a storage policy object, first call [`client.storage_policy(policy_id)`][storage_policy] to construct the 
appropriate [`Storage Policy`][storage_policy_class] object, and then calling [`storage_policy.get(*, fields=None, headers=None, **kwargs)`][get] 
will return the [`StoragePolicy`][storage_policy_class] object populated with data from the API.

<!-- sample get_storage_policies_id -->
```python
storage_policy = client.storage_policy(policy_id='12345').get()
print(f'Storage Policy ID is {storage_policy.id} and name is {storage_policy.name}')
```

[storage_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.storage_policy
[storage_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List Available Storage Policies
-------------------------------

To retrieve all storage policies for an enterprise, call [`client.get_storage_policies(limit=None, fields=None)`][get_storage_policies]. 
This method returns a `BoxObjectCollection` that allows you to iterate over the [`StoragePolicy`][storage_policy_class] 
objects in the collection.

<!-- sample get_storage_policies -->
```python
storage_policies = client.get_storage_policies(limit=100)
for storage_policy in storage_policies:
    print(f'The storage policy id is {storage_policy.id} and name is {storage_policy.name}')
```

[get_storage_policies]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_storage_policies

Assign a Storage Policy to a User
---------------------------------

To assign a storage policy to a user, call [`storage_policy.assign(user)`][assign] will create a 
[`StoragePolicyAssignment`][storage_policy_assignment_class] object with data populated from the API.

<!-- sample post_storage_policy_assignments -->
```python
user = client.user(user_id='12345')
assignment = client.storage_policy(policy_id='56781').assign(user)
print(f'Assignment ID is {assignment.id} and the assignee id is {assignment.assigned_to.id}')
```

If you know the user does not have a storage policy assigned you can directly create a storage policy assignment by calling
[`storage_policy.create_assignment(user)`][create_assignment] will create a [StoragePolicyAssignment][storage_policy_assignment_class] 
object with data populated from the API.

```python
user = client.user('56781')
assignment = client.storage_policy(policy_id='12345').create_assignment(user)
print(f'Storage Policy Assignment ID is {assignment.id} and the assignee ID is {assignment.assigned_to.id}')
```

If the user already has an assignment, you can call [storage_policy_assignment.update_info(data=updated_storage_policy)][update_info]
with a `dict` of properties to update on the storage policy assignment. This method returns a newly update 
[`StoragePolicyAssignment`][storage_policy_assignment] object with data populated from the API, leaving the original 
object unmodified.

<!-- sample put_storage_policy_assignments_id -->
```python
updated_storage_policy = {'storage_policy': {'type': 'storage_policy', 'id': '12345'}}
updated_assignment = client.storage_policy_assignment(assignment_id='ZW50ZXJwcmldfgeV82MDMwMDQ=').update_info(data=updated_storage_policy)
print(f'Update storage policy ID is {updated_assignment.storage_policy.id}')
```

[user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.user
[create_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy.create_assignment
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy_assignment.StoragePolicyAssignment
[assign]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy.assign

Get Assignment Information about a Storage Policy Assignment
------------------------------------------------------------

To get a storage policy assignment object, first call [`client.storage_policy_assignment(assignment_id)`][storage_policy_assignment] 
to construct the appropriate [`Storage Policy Assignment`][storage_policy_assignment_class] object, and then calling 
[`storage_policy_assignment.get(*, fields=None, headers=None, **kwargs)`][get] will return the [`StoragePolicyAssignment`][storage_policy_assignment_class] 
object populated with data from the API.

<!-- sample get_storage_policy_assignments_id -->
```python
assignment = client.storage_policy_assignment(assignment_id='12345').get()
print(f'Assignment ID is {assignment.id} and the storage policy ID is {assignment.storage_policy.id}')
```

[storage_policy_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.storage_policy_assignment
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy_assignment.StoragePolicyAssignment
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Get Assignment for User
-------------------------

To get a storage policy assignment object for a user, calling [`user.get_storage_policy_assignment()`][user_assignment] will 
return the [`StoragePolicyAssignment`][storage_policy_assignment_class] object populated with data from the API.

<!-- sample get_storage_policy_assignments -->
```python
assignment = client.user(user_id='12345').get_storage_policy_assignment()
print(f'Assignment ID is {assignment.id} and the storage policy ID is {assignment.storage_policy.id}')
```

[user_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.get_storage_policy_assignment
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.get_storage_policy_assignment

Delete Assignment
-----------------

To delete a storage policy assignment, call [`storage_policy_assignment.delete()`][delete]. This method returns `True` 
to indicate that the deletion was successful.

<!-- sample delete_storage_policy_assignments_id -->
```python
client.storage_policy_assignment(assignment_id='12345').delete()
print('The storage policy assignment was successfully delete!')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete
