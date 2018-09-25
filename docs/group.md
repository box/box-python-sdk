Groups
======

Groups are sets of users that can be used in collaborations.


Get All Groups
--------------

Calling `client.groups(name=None, offset=0, limit=None, fields=None)` will return an iterable of all groups in the enterprise.

```python
groups = client.groups()
for group in groups:
    # Do something
```

Alternatively, you can set a filter on the name of the groups to return from the enterprise by using `client.groups(name)`.

```python
group_name = 'Example Group'
groups = client.groups(group_name)
for group in groups:
    # Do something
```

Create a Group
--------------

To create a group, use `client.create_group(name)`.

```python
created_group = client.create_group('Example Group')
```

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

To retrieve all collaborations for a specified group call `group.collaborations(limit=None, offset=None, fields=None)`.

```python
group_id = '1234'
collaborations = client.group(group_id).collaborations()
for collaboration in collaborations:
    # Do something
```

Add User to Group
-----------------

To add a new member to the group use `group.add_member(user, role='Member')`.

```python
group_id = '1234'
user = {'id': '1111', 'type': 'user'}
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
group_id == '1111'
group_memberships = client.group(group_id).get_memberships()
for group_membership in group_memberships:
    # Do something
```

List Memberships for User
-------------------------

To retrieve all of the members for a give user use `user.get_memberships(limit=None, offset=0, fields=None)`.

```python
user_id == '2222'
user_memberships = client.user(user_id).get_group_memberships()
for user_membership in user_memberships:
    # Do something
```