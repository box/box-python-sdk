# LegalHoldPolicyAssignmentsManager

- [List legal hold policy assignments](#list-legal-hold-policy-assignments)
- [Assign legal hold policy](#assign-legal-hold-policy)
- [Get legal hold policy assignment](#get-legal-hold-policy-assignment)
- [Unassign legal hold policy](#unassign-legal-hold-policy)
- [List files with current file versions for legal hold policy assignment](#list-files-with-current-file-versions-for-legal-hold-policy-assignment)

## List legal hold policy assignments

Retrieves a list of items a legal hold policy has been assigned to.

This operation is performed by calling function `get_legal_hold_policy_assignments`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-legal-hold-policy-assignments/).

<!-- sample get_legal_hold_policy_assignments -->

```python
client.legal_hold_policy_assignments.get_legal_hold_policy_assignments(legal_hold_policy_id)
```

### Arguments

- policy_id `str`
  - The ID of the legal hold policy.
- assign_to_type `Optional[GetLegalHoldPolicyAssignmentsAssignToType]`
  - Filters the results by the type of item the policy was applied to.
- assign_to_id `Optional[str]`
  - Filters the results by the ID of item the policy was applied to.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `LegalHoldPolicyAssignments`.

Returns a list of legal hold policy assignments.

## Assign legal hold policy

Assign a legal hold to a file, file version, folder, or user.

This operation is performed by calling function `create_legal_hold_policy_assignment`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-legal-hold-policy-assignments/).

<!-- sample post_legal_hold_policy_assignments -->

```python
client.legal_hold_policy_assignments.create_legal_hold_policy_assignment(legal_hold_policy_id, CreateLegalHoldPolicyAssignmentAssignTo(type=CreateLegalHoldPolicyAssignmentAssignToTypeField.FILE, id=file_id))
```

### Arguments

- policy_id `str`
  - The ID of the policy to assign.
- assign_to `CreateLegalHoldPolicyAssignmentAssignTo`
  - The item to assign the policy to.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `LegalHoldPolicyAssignment`.

Returns a new legal hold policy assignment.

## Get legal hold policy assignment

Retrieve a legal hold policy assignment.

This operation is performed by calling function `get_legal_hold_policy_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-legal-hold-policy-assignments-id/).

<!-- sample get_legal_hold_policy_assignments_id -->

```python
client.legal_hold_policy_assignments.get_legal_hold_policy_assignment_by_id(legal_hold_policy_assignment_id)
```

### Arguments

- legal_hold_policy_assignment_id `str`
  - The ID of the legal hold policy assignment. Example: "753465"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `LegalHoldPolicyAssignment`.

Returns a legal hold policy object.

## Unassign legal hold policy

Remove a legal hold from an item.

This is an asynchronous process. The policy will not be
fully removed yet when the response returns.

This operation is performed by calling function `delete_legal_hold_policy_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-legal-hold-policy-assignments-id/).

<!-- sample delete_legal_hold_policy_assignments_id -->

```python
client.legal_hold_policy_assignments.delete_legal_hold_policy_assignment_by_id(legal_hold_policy_assignment_id)
```

### Arguments

- legal_hold_policy_assignment_id `str`
  - The ID of the legal hold policy assignment. Example: "753465"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the assignment was
successfully deleted.

## List files with current file versions for legal hold policy assignment

Get a list of files with current file versions for a legal hold
assignment.

In some cases you may want to get previous file versions instead. In these
cases, use the `GET  /legal_hold_policy_assignments/:id/file_versions_on_hold`
API instead to return any previous versions of a file for this legal hold
policy assignment.

Due to ongoing re-architecture efforts this API might not return all file
versions held for this policy ID. Instead, this API will only return the
latest file version held in the newly developed architecture. The `GET
/file_version_legal_holds` API can be used to fetch current and past versions
of files held within the legacy architecture.

This endpoint does not support returning any content that is on hold due to
a Custodian collaborating on a Hub.

The `GET /legal_hold_policy_assignments?policy_id={id}` API can be used to
find a list of policy assignments for a given policy ID.

This operation is performed by calling function `get_legal_hold_policy_assignment_file_on_hold`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-legal-hold-policy-assignments-id-files-on-hold/).

<!-- sample get_legal_hold_policy_assignments_id_files_on_hold -->

```python
client.legal_hold_policy_assignments.get_legal_hold_policy_assignment_file_on_hold(legal_hold_policy_assignment_id)
```

### Arguments

- legal_hold_policy_assignment_id `str`
  - The ID of the legal hold policy assignment. Example: "753465"
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FilesOnHold`.

Returns the list of current file versions held under legal hold for a
specific legal hold policy assignment.
