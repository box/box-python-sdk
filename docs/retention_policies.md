# RetentionPoliciesManager

- [List retention policies](#list-retention-policies)
- [Create retention policy](#create-retention-policy)
- [Get retention policy](#get-retention-policy)
- [Update retention policy](#update-retention-policy)
- [Delete retention policy](#delete-retention-policy)

## List retention policies

Retrieves all of the retention policies for an enterprise.

This operation is performed by calling function `get_retention_policies`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-retention-policies/).

<!-- sample get_retention_policies -->

```python
client.retention_policies.get_retention_policies()
```

### Arguments

- policy_name `Optional[str]`
  - Filters results by a case sensitive prefix of the name of retention policies.
- policy_type `Optional[GetRetentionPoliciesPolicyType]`
  - Filters results by the type of retention policy.
- created_by_user_id `Optional[str]`
  - Filters results by the ID of the user who created policy.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `RetentionPolicies`.

Returns a list retention policies in the enterprise.

## Create retention policy

Creates a retention policy.

This operation is performed by calling function `create_retention_policy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-retention-policies/).

<!-- sample post_retention_policies -->

```python
client.retention_policies.create_retention_policy(
    retention_policy_name,
    CreateRetentionPolicyPolicyType.FINITE,
    CreateRetentionPolicyDispositionAction.REMOVE_RETENTION,
    description=retention_description,
    retention_length="1",
    retention_type=CreateRetentionPolicyRetentionType.MODIFIABLE,
    can_owner_extend_retention=True,
    are_owners_notified=True,
)
```

### Arguments

- policy_name `str`
  - The name for the retention policy.
- description `Optional[str]`
  - The additional text description of the retention policy.
- policy_type `CreateRetentionPolicyPolicyType`
  - The type of the retention policy. A retention policy type can either be `finite`, where a specific amount of time to retain the content is known upfront, or `indefinite`, where the amount of time to retain the content is still unknown.
- disposition_action `CreateRetentionPolicyDispositionAction`
  - The disposition action of the retention policy. `permanently_delete` deletes the content retained by the policy permanently. `remove_retention` lifts retention policy from the content, allowing it to be deleted by users once the retention policy has expired.
- retention_length `Optional[str]`
  - The length of the retention policy. This value specifies the duration in days that the retention policy will be active for after being assigned to content. If the policy has a `policy_type` of `indefinite`, the `retention_length` will also be `indefinite`.
- retention_type `Optional[CreateRetentionPolicyRetentionType]`
  - Specifies the retention type: _ `modifiable`: You can modify the retention policy. For example, you can add or remove folders, shorten or lengthen the policy duration, or delete the assignment. Use this type if your retention policy is not related to any regulatory purposes. _ `non_modifiable`: You can modify the retention policy only in a limited way: add a folder, lengthen the duration, retire the policy, change the disposition action or notification settings. You cannot perform other actions, such as deleting the assignment or shortening the policy duration. Use this type to ensure compliance with regulatory retention policies.
- can_owner_extend_retention `Optional[bool]`
  - Whether the owner of a file will be allowed to extend the retention.
- are_owners_notified `Optional[bool]`
  - Whether owner and co-owners of a file are notified when the policy nears expiration.
- custom_notification_recipients `Optional[List[UserMini]]`
  - A list of users notified when the retention policy duration is about to end.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `RetentionPolicy`.

Returns a new retention policy object.

## Get retention policy

Retrieves a retention policy.

This operation is performed by calling function `get_retention_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-retention-policies-id/).

<!-- sample get_retention_policies_id -->

```python
client.retention_policies.get_retention_policy_by_id(retention_policy.id)
```

### Arguments

- retention_policy_id `str`
  - The ID of the retention policy. Example: "982312"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `RetentionPolicy`.

Returns the retention policy object.

## Update retention policy

Updates a retention policy.

This operation is performed by calling function `update_retention_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-retention-policies-id/).

<!-- sample put_retention_policies_id -->

```python
client.retention_policies.update_retention_policy_by_id(
    retention_policy.id, policy_name=updated_retention_policy_name
)
```

### Arguments

- retention_policy_id `str`
  - The ID of the retention policy. Example: "982312"
- policy_name `Optional[str]`
  - The name for the retention policy.
- description `Optional[str]`
  - The additional text description of the retention policy.
- disposition_action `Optional[str]`
  - The disposition action of the retention policy. This action can be `permanently_delete`, which will cause the content retained by the policy to be permanently deleted, or `remove_retention`, which will lift the retention policy from the content, allowing it to be deleted by users, once the retention policy has expired. You can use `null` if you don't want to change `disposition_action`.
- retention_type `Optional[str]`
  - Specifies the retention type: _ `modifiable`: You can modify the retention policy. For example, you can add or remove folders, shorten or lengthen the policy duration, or delete the assignment. Use this type if your retention policy is not related to any regulatory purposes. _ `non-modifiable`: You can modify the retention policy only in a limited way: add a folder, lengthen the duration, retire the policy, change the disposition action or notification settings. You cannot perform other actions, such as deleting the assignment or shortening the policy duration. Use this type to ensure compliance with regulatory retention policies. When updating a retention policy, you can use `non-modifiable` type only. You can convert a `modifiable` policy to `non-modifiable`, but not the other way around.
- retention_length `Optional[str]`
  - The length of the retention policy. This value specifies the duration in days that the retention policy will be active for after being assigned to content. If the policy has a `policy_type` of `indefinite`, the `retention_length` will also be `indefinite`.
- status `Optional[str]`
  - Used to retire a retention policy. If not retiring a policy, do not include this parameter or set it to `null`.
- can_owner_extend_retention `Optional[bool]`
  - Determines if the owner of items under the policy can extend the retention when the original retention duration is about to end.
- are_owners_notified `Optional[bool]`
  - Determines if owners and co-owners of items under the policy are notified when the retention duration is about to end.
- custom_notification_recipients `Optional[List[UserBase]]`
  - A list of users notified when the retention duration is about to end.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `RetentionPolicy`.

Returns the updated retention policy object.

## Delete retention policy

Permanently deletes a retention policy.

This operation is performed by calling function `delete_retention_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-retention-policies-id/).

<!-- sample delete_retention_policies_id -->

```python
client.retention_policies.delete_retention_policy_by_id(retention_policy.id)
```

### Arguments

- retention_policy_id `str`
  - The ID of the retention policy. Example: "982312"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the policy has been deleted.
