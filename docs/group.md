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
- [Update Membership](#update-membership)
- [Remove User from Group](#remove-user-from-group)
- [List Group Members](#list-group-members)
- [List Memberships for User](#list-memberships-for-user)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Groups
-----------

Calling `client.get_groups(name=None, limit=None, offset=None, fields=None)` will return an iterable of all groups in the enterprise.

```python
groups = client.get_groups()
for group in groups:
    # Do something
```

Alternatively, you can set a filter on the name of the groups to return from the enterprise by using `client.get_groups(name)`.

```python
group_name = 'Example Group'
groups = client.get_groups(group_name)
for group in groups:
    # Do something
```

Create a Group
--------------

To create a group, use `client.create_group(name, provenance=None, external_sync_identifier=None, description=None, invitability_level=None, member_viewability_level=None, fields=None)`.

```python
created_group = client.create_group('Example Group')
```

You can read more about the optional parameters [here](https://developer.box.com/v2.0/reference#create-a-group)

Get Information about a Group
-----------------------------

To retrieve information about a group use `group.get()`.

```python
group_id = '1111'
group_information = client.group(group_id).get()
```

Update a Group
--------------

To update a group call `group.update_info()`.

```python
group_id = '1234'
group_update = {'name': 'New Group Name'}
updated_group = client.group(group_id).update_info(group_update)
```

Delete a Group
--------------

To delete a specified group call `group.delete()`.

```python
group_id = '1234'
client.group(group_id).delete()
```

Get a Group's Collaborations
----------------------------

To retrieve all collaborations for a specified group call `group.get_collaborations(limit=None, offset=None, fields=None)`.

```python
group_id = '1234'
collaborations = client.group(group_id).get_collaborations()
for collaboration in collaborations:
    # Do something
```

Add User to Group
-----------------

To add a new member to the group use `group.add_member(user, role='Member', configurable_permissions=None)`.

```python
group_id = '1234'
user = client.user('1111')
group_membership = client.group(group_id).add_member(user)
```

Get Information about a Group Membership
----------------------------------------

To retrieve information about a group_membership, use `group_membership.get()`.

```python
membership_id = '1111'
membership_info = client.group_membership(membership_id).get()
```

Update Membership
-----------------

To update a group membership, use `group_membership.update_info()`.

```python
membership_id = '1234'
membership_update = {'role': 'admin'}
updated_membership_info = client.group_membership.update_info(membership_update)
```

Remove User from Group
----------------------

To delete a group membership use, `group_membership.delete()`. This removes a specific user from a group.

```python
membership_id = '1234'
client.group_membership(membership_id).delete() 
```

List Group Members
------------------

To retrieve all of the members for a given group use `group.get_memberships(limit=None, offset=0, fields=None)`.

```python
group_id = '1111'
group_memberships = client.group(group_id).get_memberships()
for group_membership in group_memberships:
    # Do something
```

List Memberships for User
-------------------------

To retrieve all of the members for a give user use `user.get_group_memberships(limit=None, offset=0, fields=None)`.

```python
user_id = '2222'
user_memberships = client.user(user_id).get_group_memberships()
for user_membership in user_memberships:
    # Do something
```
