# MembershipsManager

- [List user's groups](#list-users-groups)
- [List members of group](#list-members-of-group)
- [Add user to group](#add-user-to-group)
- [Get group membership](#get-group-membership)
- [Update group membership](#update-group-membership)
- [Remove user from group](#remove-user-from-group)

## List user's groups

Retrieves all the groups for a user. Only members of this
group or users with admin-level permissions will be able to
use this API.

This operation is performed by calling function `get_user_memberships`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-users-id-memberships/).

<!-- sample get_users_id_memberships -->

```python
client.memberships.get_user_memberships(user.id)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- limit `Optional[int]`
  - The maximum number of items to return per page.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupMemberships`.

Returns a collection of membership objects. If there are no
memberships, an empty collection will be returned.

## List members of group

Retrieves all the members for a group. Only members of this
group or users with admin-level permissions will be able to
use this API.

This operation is performed by calling function `get_group_memberships`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-groups-id-memberships/).

<!-- sample get_groups_id_memberships -->

```python
client.memberships.get_group_memberships(group.id)
```

### Arguments

- group_id `str`
  - The ID of the group. Example: "57645"
- limit `Optional[int]`
  - The maximum number of items to return per page.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupMemberships`.

Returns a collection of membership objects. If there are no
memberships, an empty collection will be returned.

## Add user to group

Creates a group membership. Only users with
admin-level permissions will be able to use this API.

This operation is performed by calling function `create_group_membership`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-group-memberships/).

<!-- sample post_group_memberships -->

```python
client.memberships.create_group_membership(
    CreateGroupMembershipUser(id=user.id), CreateGroupMembershipGroup(id=group.id)
)
```

### Arguments

- user `CreateGroupMembershipUser`
  - The user to add to the group.
- group `CreateGroupMembershipGroup`
  - The group to add the user to.
- role `Optional[CreateGroupMembershipRole]`
  - The role of the user in the group.
- configurable_permissions `Optional[Dict[str, bool]]`
  - Custom configuration for the permissions an admin if a group will receive. This option has no effect on members with a role of `member`. Setting these permissions overwrites the default access levels of an admin. Specifying a value of `null` for this object will disable all configurable permissions. Specifying permissions will set them accordingly, omitted permissions will be enabled by default.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupMembership`.

Returns a new group membership object.

## Get group membership

Retrieves a specific group membership. Only admins of this
group or users with admin-level permissions will be able to
use this API.

This operation is performed by calling function `get_group_membership_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-group-memberships-id/).

<!-- sample get_group_memberships_id -->

```python
client.memberships.get_group_membership_by_id(group_membership.id)
```

### Arguments

- group_membership_id `str`
  - The ID of the group membership. Example: "434534"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupMembership`.

Returns the group membership object.

## Update group membership

Updates a user's group membership. Only admins of this
group or users with admin-level permissions will be able to
use this API.

This operation is performed by calling function `update_group_membership_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-group-memberships-id/).

<!-- sample put_group_memberships_id -->

```python
client.memberships.update_group_membership_by_id(
    group_membership.id, role=UpdateGroupMembershipByIdRole.ADMIN
)
```

### Arguments

- group_membership_id `str`
  - The ID of the group membership. Example: "434534"
- role `Optional[UpdateGroupMembershipByIdRole]`
  - The role of the user in the group.
- configurable_permissions `Optional[Dict[str, bool]]`
  - Custom configuration for the permissions an admin if a group will receive. This option has no effect on members with a role of `member`. Setting these permissions overwrites the default access levels of an admin. Specifying a value of `null` for this object will disable all configurable permissions. Specifying permissions will set them accordingly, omitted permissions will be enabled by default.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupMembership`.

Returns a new group membership object.

## Remove user from group

Deletes a specific group membership. Only admins of this
group or users with admin-level permissions will be able to
use this API.

This operation is performed by calling function `delete_group_membership_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-group-memberships-id/).

<!-- sample delete_group_memberships_id -->

```python
client.memberships.delete_group_membership_by_id(group_membership.id)
```

### Arguments

- group_membership_id `str`
  - The ID of the group membership. Example: "434534"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the membership was
successfully deleted.
