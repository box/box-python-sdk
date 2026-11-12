# InvitesManager

- [Create user invite](#create-user-invite)
- [Get user invite status](#get-user-invite-status)

## Create user invite

Invites an existing external user to join an enterprise.

The user must already have a Box account and cannot be
part of another enterprise. Once invited, the user receives
an email and is prompted to accept the invitation in
the Box web application.

If `is_auto_roll_in_enabled` is set to `true`, the user does not have to
accept the invitation and is added to the enterprise automatically after
14 days. Only unmanaged users can be invited this way. An unmanaged user
is a free user whose email domain matches one of the enterprise's
domains. Availability depends on the enterprise's plan.

This method requires the "Manage An Enterprise" scope enabled for
the application, which can be enabled within the developer console.

This operation is performed by calling function `create_invite`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-invites/).

<!-- sample post_invites -->

```python
client.invites.create_invite(
    CreateInviteEnterprise(id=current_user.enterprise.id),
    CreateInviteActionableBy(login=email),
)
```

### Arguments

- enterprise `CreateInviteEnterprise`
  - The enterprise to invite the user to.
- actionable_by `CreateInviteActionableBy`
  - The user to invite.
- is_auto_roll_in_enabled `Optional[bool]`
  - If set to `true`, the user is added to the enterprise automatically after 14 days instead of having to accept the invite. Only unmanaged users can be invited this way. Availability depends on the enterprise's plan.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Invite`.

Returns a new invite object.

## Get user invite status

Returns the status of a user invite.

This operation is performed by calling function `get_invite_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-invites-id/).

<!-- sample get_invites_id -->

```python
client.invites.get_invite_by_id(invitation.id)
```

### Arguments

- invite_id `str`
  - The ID of an invite. Example: "213723"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Invite`.

Returns an invite object.
