Storage Policy 
==============

Allows the enterprise admin to manage the Storage Policies for users in their
enterprise. Used for an enterprise to decide storage location for users based on
where they work/reside. 


Get Storage Policy
------------------

To get a storage policy object, first call [`client.storage_policy(policy_id)`][storage_policy] to construct the appropriate [`Storage Policy`][storage_policy_class] object, and then calling [`storage_policy.get(fields=None)`][get] will return the [`Storage Policy`][storage_policy_class] object populated with data from the API.

```python
storage_policy = client.storage_policy('12345').get()
print('Storage Policy id is {0} and name is {1}'.format(storage_policy.id, storage_policy.name))
```

[storage_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.Client.storage_policy
[storage_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List Available Storage Policies
-------------------------------

To retrieve all storage policies for an enterprise, call [`client.get_storage_policies(limit=None, fields=None)`][get_storage_policies]. This method returns a `BoxObjectCollection` that allows you to iterate over the [`Storage Policy`][storage_policy_class] objects in the collection.

```python
storage_policies = client.get_storage_policies(limit=100)
for storage_policy in storage_policies:
    print('The storage policy id is {0} and name is {1}'.format(storage_policy.id, storage_policy.name)))
```

[get_storage_policies]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.get_storage_policies
[storage_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy

Create Storage Policy Assignment
--------------------------------

To create a storage policy assignment object, call [`client.storage_policy(policy_id)`][storage_policy] to construct the appropriate [`Storage Policy`][storage_policy_class] object. Then call [`client.user(user_id)`][user] to create the user you wish to assign the storage policy to. Finally calling [`storage_policy.create_assignment(user)`][create_assignment] will create a [Storage Policy Assignment][storage_policy_assignment_class] object with data populated from the API.

```python
user = client.user('56781')
storage_policy_assignment = client.storage_policy('12345').create_assignment(user)
print('Storage Policy Assignment id is {0} and the assignee id is {1}'.format(storage_policy_assignment.id, storage_policy_assignment.assigned_to.id))
```

Note: This method only works if the user does not already have an assignment. If the current state of the user is not known, use the [`storage_policy.assign(user)`][assign] method instead.

[storage_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.Client.storage_policy
[storage_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy
[user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.user
[create_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy.create_assignment
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy_assignment.StoragePolicyAssignment
[assign]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.assign

Assign a Storage Policy to a User
---------------------------------

To assign a storage policy to a user, first call [`client.storage_policy(policy_id)`][storage_policy] to construct the appropriate [`Storage Policy`][storage_policy_class] object. Then call [`client.user(user_id)`][user] to construct the user you wish to assign the storage policy to. Finally calling [`storage_policy.assign(user)`][assign] will create a [`Storage Policy Assignment`][storage_policy_assignment_class] object with data populated from the API.

```python
user = client.user('12345')
storage_policy_assignment = client.storage_policy('56781').assign(user)
print('Assignment id is {0} and the assignee id is {1}'.format(storage_policy_assignment.id, storage_policy_assignment.assigned_to.id))
```

[storage_policy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.Client.storage_policy
[storage_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy.StoragePolicy
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy_assignment.StoragePolicyAssignment
[user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.Client.user
[assign]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.object.storage_policy.StoragePolicy.assign

Update Existing Assignment
--------------------------

To update a storage policy object, first call [`client.storage_policy_assignment(assignment_id)`][storage_policy_assignment] to construct the appropriate [`Storage Policy Assignmennt`][storage_policy_assignment_class] object, and then calling [storage_policy_assignment.update_info(data)][update_info] with a `dict` of properties to update on the storage policy assignment. This method returns a newly update [`Storage Policy Assignment`][storage_policy_assignment] object, leaving the original object unmodified.

```python
updated_storage_policy = {'storage_policy': {'type': 'storage_policy', 'id': '12345'}}
updated_assignment = client.storage_policy_assignment('ZW50ZXJwcmldfgeV82MDMwMDQ=').update_info(updated_storage_policy)
print('Update storage policy id is {0}'.format(updated_assignment.storage_policy.id))
```

[storage_policy_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.storage_policy_assignment
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy_assignment.StoragePolicyAssignment
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Get Assignment
--------------

To get a storage policy assignment object, first call [`client.storage_policy_assignment(assignment_id)`][storage_policy_assignment] to construct the appropriate [`Storage Policy Assignment`][storage_policy_assignment_class] object, and then calling [`storage_policy_assignment.get(fields=None)`][get] will return the [`Storage Policy Assignment`][storage_policy_assignment_class] object populated with data from the API.

```python
assignment = client.storage_policy_assignment('12345').get()
print('Assignment id is {0} and the storage policy id is {1}'.format(assignment.id, assignment.storage_policy.id))
```

[storage_policy_assignment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.storage_policy_assignment
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.storage_policy_assignment.StoragePolicyAssignment
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Get Assignment for User
-------------------------

To get a storage policy assignment object for a user, first call [`client.user(user_id)`][user] to construct the appropriate [`User`][user_class] object, and then calling [`user.get_storage_policy_assignment()`][user_assignment] will return the [`Storage Policy Assignment`][storage_policy_assignment_class] object populated with data from the API.

```python
assignment = client.user('12345').get_storage_policy_assignment()
print('Assignment id is {0} and the storage policy id is {1}'.format(assignment.id, assignment.storage_policy.id))
```

[user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.client.Client.user
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User
[storage_policy_assignment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.get_storage_policy_assignment

Delete Assignment
-----------------

To delete a storage policy assignment, call [`storage_policy_assignment.delete()`][delete]. This method returns `True` to indicate that the deletion was successful.

```python
client.storage_policy_assignment('12345').delete()
print('The storage policy assignment was successfully delete!')
```
