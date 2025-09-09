# LegalHoldPoliciesManager

- [List all legal hold policies](#list-all-legal-hold-policies)
- [Create legal hold policy](#create-legal-hold-policy)
- [Get legal hold policy](#get-legal-hold-policy)
- [Update legal hold policy](#update-legal-hold-policy)
- [Remove legal hold policy](#remove-legal-hold-policy)

## List all legal hold policies

Retrieves a list of legal hold policies that belong to
an enterprise.

This operation is performed by calling function `get_legal_hold_policies`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-legal-hold-policies/).

<!-- sample get_legal_hold_policies -->

```python
client.legal_hold_policies.get_legal_hold_policies()
```

### Arguments

- policy_name `Optional[str]`
  - Limits results to policies for which the names start with this search term. This is a case-insensitive prefix.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `LegalHoldPolicies`.

Returns a list of legal hold policies.

## Create legal hold policy

Create a new legal hold policy.

This operation is performed by calling function `create_legal_hold_policy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-legal-hold-policies/).

<!-- sample post_legal_hold_policies -->

```python
client.legal_hold_policies.create_legal_hold_policy(legal_hold_policy_name, description=legal_hold_description, filter_started_at=filter_started_at, filter_ended_at=filter_ended_at, is_ongoing=False)
```

### Arguments

- policy_name `str`
  - The name of the policy.
- description `Optional[str]`
  - A description for the policy.
- filter_started_at `Optional[DateTime]`
  - The filter start date. When this policy is applied using a `custodian` legal hold assignments, it will only apply to file versions created or uploaded inside of the date range. Other assignment types, such as folders and files, will ignore the date filter. Required if `is_ongoing` is set to `false`.
- filter_ended_at `Optional[DateTime]`
  - The filter end date. When this policy is applied using a `custodian` legal hold assignments, it will only apply to file versions created or uploaded inside of the date range. Other assignment types, such as folders and files, will ignore the date filter. Required if `is_ongoing` is set to `false`.
- is_ongoing `Optional[bool]`
  - Whether new assignments under this policy should continue applying to files even after initialization. When this policy is applied using a legal hold assignment, it will continue applying the policy to any new file versions even after it has been applied. For example, if a legal hold assignment is placed on a user today, and that user uploads a file tomorrow, that file will get held. This will continue until the policy is retired. Required if no filter dates are set.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `LegalHoldPolicy`.

Returns a new legal hold policy object.

## Get legal hold policy

Retrieve a legal hold policy.

This operation is performed by calling function `get_legal_hold_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-legal-hold-policies-id/).

<!-- sample get_legal_hold_policies_id -->

```python
client.legal_hold_policies.get_legal_hold_policy_by_id(legal_hold_policy_id)
```

### Arguments

- legal_hold_policy_id `str`
  - The ID of the legal hold policy. Example: "324432"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `LegalHoldPolicy`.

Returns a legal hold policy object.

## Update legal hold policy

Update legal hold policy.

This operation is performed by calling function `update_legal_hold_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-legal-hold-policies-id/).

<!-- sample put_legal_hold_policies_id -->

```python
client.legal_hold_policies.update_legal_hold_policy_by_id(legal_hold_policy_id, policy_name=updated_legal_hold_policy_name)
```

### Arguments

- legal_hold_policy_id `str`
  - The ID of the legal hold policy. Example: "324432"
- policy_name `Optional[str]`
  - The name of the policy.
- description `Optional[str]`
  - A description for the policy.
- release_notes `Optional[str]`
  - Notes around why the policy was released.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `LegalHoldPolicy`.

Returns a new legal hold policy object.

## Remove legal hold policy

Delete an existing legal hold policy.

This is an asynchronous process. The policy will not be
fully deleted yet when the response returns.

This operation is performed by calling function `delete_legal_hold_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-legal-hold-policies-id/).

<!-- sample delete_legal_hold_policies_id -->

```python
client.legal_hold_policies.delete_legal_hold_policy_by_id(legal_hold_policy.id)
```

### Arguments

- legal_hold_policy_id `str`
  - The ID of the legal hold policy. Example: "324432"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the policy was
successfully deleted.
