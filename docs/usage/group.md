Groups
======
Groups are sets of users that can be used in collaborations.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [List Groups](#list-groups)
- [Create a Group](#create-a-group)
- [Get Information about a Group](#get-information-about-a-group)
- [Update a Group](#update-a-group)
- [Delete a Group](#delete-a-group)
- [Get a Group's Collaborations](#get-a-groups-collaborations)
- [Add User to Group](#add-user-to-group)
- [Get Information about a Group Membership](#get-information-about-a-group-membership)
- [Update Group Membership](#update-group-membership)
- [Remove User from Group](#remove-user-from-group)
- [List Group Members](#list-group-members)
- [List Memberships for User](#list-memberships-for-user)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Groups
-----------

Calling [`client.get_groups(name=None, limit=None, offset=None, fields=None)`][get_groups] will return a
`BoxObjectCollection` that allows you to iterate over the [`Group`][group_class] objects representing groups in the
enterprise.

<!-- sample get_groups -->
```python
groups = client.get_groups()
for group in groups:
    print(f'Group "{group.name}" has ID "{group.id}"')
```

Alternatively, you can set a filter on the name of the groups by passing the `name` parameter:

```python
group_name = 'Example Group'
groups = client.get_groups(group_name)
for group in groups:
    print(f'Group {group.id} has a name matching {group_name}')
```

[get_groups]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_groups
[group_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.group.Group

Create a Group
--------------

To create a new group, call
[`client.create_group(name, provenance=None, external_sync_identifier=None, description=None, invitability_level=None, member_viewability_level=None, fields=None)`][create_group] with the name of the group and any optional group properties you want to set.  This method
returns a [`Group`][group_class] object representing the created group.

You can read more about the optional parameters in the
[Create Group API documentation](https://developer.box.com/en/reference/post-groups/).

<!-- sample post_groups -->
```python
created_group = client.create_group('Example Group')
print(f'Created group with ID {created_group.id}')
```

[create_group]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_group

Get Information about a Group
-----------------------------

To retrieve information about a group, first call [`client.group(group_id)`][group] to initialize a
[`Group`][group_class] object.  Then, call [`group.get(*, fields=None, headers=None, **kwargs)`][get] to retrieve the
data about that group. This method returns a new [`Group`][group_class] object with fields populated by data form the API,
leaving the original object unmodified.

<!-- sample get_groups_id -->
```python
group = client.group(group_id='11111').get()
print(f'Got group {group.name}')
```

You can optionally specify a list of `fields` to retrieve from the API, in order to filter out fields you don't need or
add fields that are not returned from the API by default:

```python
group = client.group(group_id='11111').get(['name', 'description', 'provenance'])
print(f'The "{group.name}" group ({group.description}) came from {group.provenance}')
```

[group]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.group
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get


Update a Group
--------------

To update a group, call [`group.update_info(data=group_update)`][update_info] with a `dict` of the group properties
to update.  This method returns a new [`Group`][group_class] object with the updates applied, leaving the original
object unmodified.

<!-- sample put_groups_id -->
```python
group_update = {'name': 'New Group Name'}
updated_group = client.group(group_id='11111').update_info(data=group_update)
print(f'Changed the name of group {updated_group.id} to "{updated_group.name}"')
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Delete a Group
--------------

To delete a group, call [`group.delete()`][delete].  This method returns `True` to indicate that the deletion was
successful.

<!-- sample delete_groups_id -->
```python
client.group(group_id='11111').delete()
print('The group was deleted!')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete

Get a Group's Collaborations
----------------------------

To retrieve all collaborations for a group, call
[`group.get_collaborations(limit=None, offset=None, fields=None)`][get_collaborations].  This method returns a
`BoxObjectCollection` that allows you to iterate over the [`Collaboration`][collaboration_class] objects in the
collection.

<!-- sample get_groups_id_collaborations -->
```python
collaborations = client.group(group_id='11111').get_collaborations()
for collaboration in collaborations:
    print(f'The group is collaborated on {collaboration.item.type} {collaboration.item.id}')
```

[get_collaborations]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.group.Group.get_collaborations
[collaboration_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration.Collaboration

Add User to Group
-----------------

To add a new member to the group, call
[`group.add_member(user, role='member', configurable_permissions=None)`][add_member] with the [`User`][user_class] to
add to the group.  This method returns a new [`GroupMembership`][membership_class] object representing the presence of
the user in the group.

You can optionally specify the user's `role` in the group, and for users with an admin role you can configure which
permissions they have in the group by passing a `dict` of [group permissions][permissions] to `configurable_permissions`.

<!-- sample post_group_memberships -->
```python
user = client.user('1111')
membership = client.group(group_id='11111').add_member(user)
print(f'Added {membership.user.name} to the {membership.group.name} group!')
```

[add_member]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.group.Group.add_member
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User
[permissions]: https://developer.box.com/en/reference/resources/group-membership/

Get Information about a Group Membership
----------------------------------------

To retrieve information about a group membership, first call
[`client.group_membership(group_membership_id)`][group_membership] to initialize the
[`GroupMembership`][membership_class] object.  Then, call [`group_membership.get(*, fields=None, headers=None, **kwargs)`][get]
to retrieve data about the group membership from the API.  This returns a new [`GroupMembership`][membership_class]
object with fields populated by data from the API, leaving the original object unmodified.

<!-- sample get_group_memberships_id -->
```python
membership_id = '11111'
membership = client.group_membership(membership_id).get()
print(f'User "{membership.user.name}" is a member of the {membership.group.name} group')
```

[group_membership]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.group_membership
[membership_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.group_membership.GroupMembership

Update Group Membership
-----------------------

To update a group membership, call [`membership.update_info(data=membership_update)`][update_info] with a `dict` of
properties to update on the membership object.  This method returns a new [`GroupMembership`][membership_class] object
with the changes applied, leaving the original object unmodified.

<!-- sample put_group_memberships_id -->
```python
membership_id = '1234'
membership_update = {'role': 'admin'}
updated_membership = client.group_membership(membership_id).update_info(data=membership_update)
print(f'Updated {updated_membership.user.name}\'s group role to {updated_membership.role}')
```

Remove User from Group
----------------------

To remove a user from a group, delete their associated group membership by calling [`group_membership.delete()`][delete].
This method returns `True` to indicate that the deletion was successful.

<!-- sample delete_group_memberships_id -->
```python
membership_id = '1234'
client.group_membership(membership_id).delete() 
print('The membership was deleted!')
```

List Group Members
------------------

To retrieve all of the memberships for a given group, call
[`group.get_memberships(limit=None, offset=0, fields=None)`][get_memberships].  This method returns a
`BoxObjectCollection` that allows you to iterate over all of the [`GroupMembership`][membership_class] objects in the
collection.

<!-- sample get_groups_id_memberships -->
```python
group_memberships = client.group(group_id='11111').get_memberships()
for membership in group_memberships:
    print(f'{membership.user.name} is a {membership.role} of the {membership.group.name} group')
```

[get_memberships]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.group.Group.get_memberships

List Memberships for User
-------------------------

To retrieve all of the groups a user belongs to, get a list of their associated group memberships by calling
[`user.get_group_memberships(limit=None, offset=0, fields=None)`][get_group_memberships].  This method returns a
`BoxObjectCollection` that allows you to iterate over the [`GroupMembership`][membership_class] objects in the
collection.

<!-- sample get_users_id_memberships -->
```python
user_memberships = client.user(user_id='33333').get_group_memberships()
for membership in user_memberships:
    print(f'User is in the {membership.group.name} group')
```

[get_group_memberships]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.get_group_memberships
