# GroupsManager

- [List groups for enterprise](#list-groups-for-enterprise)
- [Create group](#create-group)
- [Get group](#get-group)
- [Update group](#update-group)
- [Remove group](#remove-group)

## List groups for enterprise

Retrieves all of the groups for a given enterprise. The user
must have admin permissions to inspect enterprise's groups.

This operation is performed by calling function `get_groups`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-groups/).

<!-- sample get_groups -->

```python
client.groups.get_groups()
```

### Arguments

- filter_term `Optional[str]`
  - Limits the results to only groups whose `name` starts with the search term.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Groups`.

Returns a collection of group objects. If there are no groups, an
empty collection will be returned.

## Create group

Creates a new group of users in an enterprise. Only users with admin
permissions can create new groups.

This operation is performed by calling function `create_group`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-groups/).

<!-- sample post_groups -->

```python
client.groups.create_group(group_name, description=group_description)
```

### Arguments

- name `str`
  - The name of the new group to be created. This name must be unique within the enterprise.
- provenance `Optional[str]`
  - Keeps track of which external source this group is coming, for example `Active Directory`, or `Okta`. Setting this will also prevent Box admins from editing the group name and its members directly via the Box web application. This is desirable for one-way syncing of groups.
- external_sync_identifier `Optional[str]`
  - An arbitrary identifier that can be used by external group sync tools to link this Box Group to an external group. Example values of this field could be an **Active Directory Object ID** or a **Google Group ID**. We recommend you use of this field in order to avoid issues when group names are updated in either Box or external systems.
- description `Optional[str]`
  - A human readable description of the group.
- invitability_level `Optional[CreateGroupInvitabilityLevel]`
  - Specifies who can invite the group to collaborate on folders. When set to `admins_only` the enterprise admin, co-admins, and the group's admin can invite the group. When set to `admins_and_members` all the admins listed above and group members can invite the group. When set to `all_managed_users` all managed users in the enterprise can invite the group.
- member_viewability_level `Optional[CreateGroupMemberViewabilityLevel]`
  - Specifies who can see the members of the group. _ `admins_only` - the enterprise admin, co-admins, group's group admin. _ `admins_and_members` - all admins and group members. \* `all_managed_users` - all managed users in the enterprise.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupFull`.

Returns the new group object.

## Get group

Retrieves information about a group. Only members of this
group or users with admin-level permissions will be able to
use this API.

This operation is performed by calling function `get_group_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-groups-id/).

<!-- sample get_groups_id -->

```python
client.groups.get_group_by_id(group.id, fields=['id', 'name', 'description', 'group_type'])
```

### Arguments

- group_id `str`
  - The ID of the group. Example: "57645"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupFull`.

Returns the group object.

## Update group

Updates a specific group. Only admins of this
group or users with admin-level permissions will be able to
use this API.

This operation is performed by calling function `update_group_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-groups-id/).

<!-- sample put_groups_id -->

```python
client.groups.update_group_by_id(group.id, name=updated_group_name)
```

### Arguments

- group_id `str`
  - The ID of the group. Example: "57645"
- name `Optional[str]`
  - The name of the new group to be created. Must be unique within the enterprise.
- provenance `Optional[str]`
  - Keeps track of which external source this group is coming, for example `Active Directory`, or `Okta`. Setting this will also prevent Box admins from editing the group name and its members directly via the Box web application. This is desirable for one-way syncing of groups.
- external_sync_identifier `Optional[str]`
  - An arbitrary identifier that can be used by external group sync tools to link this Box Group to an external group. Example values of this field could be an **Active Directory Object ID** or a **Google Group ID**. We recommend you use of this field in order to avoid issues when group names are updated in either Box or external systems.
- description `Optional[str]`
  - A human readable description of the group.
- invitability_level `Optional[UpdateGroupByIdInvitabilityLevel]`
  - Specifies who can invite the group to collaborate on folders. When set to `admins_only` the enterprise admin, co-admins, and the group's admin can invite the group. When set to `admins_and_members` all the admins listed above and group members can invite the group. When set to `all_managed_users` all managed users in the enterprise can invite the group.
- member_viewability_level `Optional[UpdateGroupByIdMemberViewabilityLevel]`
  - Specifies who can see the members of the group. _ `admins_only` - the enterprise admin, co-admins, group's group admin. _ `admins_and_members` - all admins and group members. \* `all_managed_users` - all managed users in the enterprise.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `GroupFull`.

Returns the updated group object.

## Remove group

Permanently deletes a group. Only users with
admin-level permissions will be able to use this API.

This operation is performed by calling function `delete_group_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-groups-id/).

<!-- sample delete_groups_id -->

```python
client.groups.delete_group_by_id(group.id)
```

### Arguments

- group_id `str`
  - The ID of the group. Example: "57645"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the group was
successfully deleted.
