# CollaborationAllowlistExemptTargetsManager

- [List users exempt from collaboration domain restrictions](#list-users-exempt-from-collaboration-domain-restrictions)
- [Create user exemption from collaboration domain restrictions](#create-user-exemption-from-collaboration-domain-restrictions)
- [Get user exempt from collaboration domain restrictions](#get-user-exempt-from-collaboration-domain-restrictions)
- [Remove user from list of users exempt from domain restrictions](#remove-user-from-list-of-users-exempt-from-domain-restrictions)

## List users exempt from collaboration domain restrictions

Returns a list of users who have been exempt from the collaboration
domain restrictions.

This operation is performed by calling function `get_collaboration_whitelist_exempt_targets`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collaboration-whitelist-exempt-targets/).

<!-- sample get_collaboration_whitelist_exempt_targets -->

```python
client.collaboration_allowlist_exempt_targets.get_collaboration_whitelist_exempt_targets()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationAllowlistExemptTargets`.

Returns a collection of user exemptions.

## Create user exemption from collaboration domain restrictions

Exempts a user from the restrictions set out by the allowed list of domains
for collaborations.

This operation is performed by calling function `create_collaboration_whitelist_exempt_target`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-collaboration-whitelist-exempt-targets/).

<!-- sample post_collaboration_whitelist_exempt_targets -->

```python
client.collaboration_allowlist_exempt_targets.create_collaboration_whitelist_exempt_target(CreateCollaborationWhitelistExemptTargetUser(id=user.id))
```

### Arguments

- user `CreateCollaborationWhitelistExemptTargetUser`
  - The user to exempt.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationAllowlistExemptTarget`.

Returns a new exemption entry.

## Get user exempt from collaboration domain restrictions

Returns a users who has been exempt from the collaboration
domain restrictions.

This operation is performed by calling function `get_collaboration_whitelist_exempt_target_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collaboration-whitelist-exempt-targets-id/).

<!-- sample get_collaboration_whitelist_exempt_targets_id -->

```python
client.collaboration_allowlist_exempt_targets.get_collaboration_whitelist_exempt_target_by_id(new_exempt_target.id)
```

### Arguments

- collaboration_whitelist_exempt_target_id `str`
  - The ID of the exemption to the list. Example: "984923"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationAllowlistExemptTarget`.

Returns the user's exempted from the list of collaboration domains.

## Remove user from list of users exempt from domain restrictions

Removes a user's exemption from the restrictions set out by the allowed list
of domains for collaborations.

This operation is performed by calling function `delete_collaboration_whitelist_exempt_target_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-collaboration-whitelist-exempt-targets-id/).

<!-- sample delete_collaboration_whitelist_exempt_targets_id -->

```python
client.collaboration_allowlist_exempt_targets.delete_collaboration_whitelist_exempt_target_by_id(exempt_target.id)
```

### Arguments

- collaboration_whitelist_exempt_target_id `str`
  - The ID of the exemption to the list. Example: "984923"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the exemption was
successfully deleted.
