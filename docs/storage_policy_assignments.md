# StoragePolicyAssignmentsManager

- [List storage policy assignments](#list-storage-policy-assignments)
- [Assign storage policy](#assign-storage-policy)
- [Get storage policy assignment](#get-storage-policy-assignment)
- [Update storage policy assignment](#update-storage-policy-assignment)
- [Unassign storage policy](#unassign-storage-policy)

## List storage policy assignments

Fetches all the storage policy assignment for an enterprise or user.

This operation is performed by calling function `get_storage_policy_assignments`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-storage-policy-assignments/).

<!-- sample get_storage_policy_assignments -->

```python
client.storage_policy_assignments.get_storage_policy_assignments(
    GetStoragePolicyAssignmentsResolvedForType.USER, user_id
)
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- resolved_for_type `GetStoragePolicyAssignmentsResolvedForType`
  - The target type to return assignments for.
- resolved_for_id `str`
  - The ID of the user or enterprise to return assignments for.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `StoragePolicyAssignments`.

Returns a collection of storage policies for
the enterprise or user.

## Assign storage policy

Creates a storage policy assignment for an enterprise or user.

This operation is performed by calling function `create_storage_policy_assignment`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-storage-policy-assignments/).

<!-- sample post_storage_policy_assignments -->

```python
client.storage_policy_assignments.create_storage_policy_assignment(
    CreateStoragePolicyAssignmentStoragePolicy(id=policy_id),
    CreateStoragePolicyAssignmentAssignedTo(
        id=user_id, type=CreateStoragePolicyAssignmentAssignedToTypeField.USER
    ),
)
```

### Arguments

- storage_policy `CreateStoragePolicyAssignmentStoragePolicy`
  - The storage policy to assign to the user or enterprise.
- assigned_to `CreateStoragePolicyAssignmentAssignedTo`
  - The user or enterprise to assign the storage policy to.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `StoragePolicyAssignment`.

Returns the new storage policy assignment created.

## Get storage policy assignment

Fetches a specific storage policy assignment.

This operation is performed by calling function `get_storage_policy_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-storage-policy-assignments-id/).

<!-- sample get_storage_policy_assignments_id -->

```python
client.storage_policy_assignments.get_storage_policy_assignment_by_id(
    storage_policy_assignment.id
)
```

### Arguments

- storage_policy_assignment_id `str`
  - The ID of the storage policy assignment. Example: "932483"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `StoragePolicyAssignment`.

Returns a storage policy assignment object.

## Update storage policy assignment

Updates a specific storage policy assignment.

This operation is performed by calling function `update_storage_policy_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-storage-policy-assignments-id/).

<!-- sample put_storage_policy_assignments_id -->

```python
client.storage_policy_assignments.update_storage_policy_assignment_by_id(
    storage_policy_assignment.id,
    UpdateStoragePolicyAssignmentByIdStoragePolicy(id=storage_policy_2.id),
)
```

### Arguments

- storage_policy_assignment_id `str`
  - The ID of the storage policy assignment. Example: "932483"
- storage_policy `UpdateStoragePolicyAssignmentByIdStoragePolicy`
  - The storage policy to assign to the user or enterprise.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `StoragePolicyAssignment`.

Returns an updated storage policy assignment object.

## Unassign storage policy

Delete a storage policy assignment.

Deleting a storage policy assignment on a user
will have the user inherit the enterprise's default
storage policy.

There is a rate limit for calling this endpoint of only
twice per user in a 24 hour time frame.

This operation is performed by calling function `delete_storage_policy_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-storage-policy-assignments-id/).

<!-- sample delete_storage_policy_assignments_id -->

```python
client.storage_policy_assignments.delete_storage_policy_assignment_by_id(
    storage_policy_assignment.id
)
```

### Arguments

- storage_policy_assignment_id `str`
  - The ID of the storage policy assignment. Example: "932483"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the storage policy
assignment is successfully deleted.
