Users
=====

Users represent an individual's account on Box.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get User Information](#get-user-information)
- [Get the Current User's Information](#get-the-current-users-information)
- [Create An Enterprise User](#create-an-enterprise-user)
- [Get the Avatar for a User](#get-the-avatar-for-a-user)
- [Create An App User](#create-an-app-user)
- [Update User](#update-user)
- [Delete User](#delete-user)
- [Invite User to Enterprise](#invite-user-to-enterprise)
- [Get Email Aliases](#get-email-aliases)
- [Add Email Alias](#add-email-alias)
- [Remove Email Alias](#remove-email-alias)
- [Get Enterprise Users](#get-enterprise-users)
- [Transfer User Content](#transfer-user-content)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get User Information
--------------------

To get information about a user, call the [`user.get(*, fields=None, headers=None, **kwargs)`][object_get] method.
This method returns a new [`User`][user_class] object with fields populated by data from the API.

<!-- sample get_users_id -->
```python
user_id = '33333'
user = client.user(user_id).get()
```

You can specify which fields on the `User` object you want by passing an `Iterable` of field names:

```python
user_id = '33333'
user = client.user(user_id).get(['id', 'name', 'login', 'is_sync_enabled'])

if user.is_sync_enabled:
    print(f'User {user.id} has sync enabled')
```

[object_get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User

Get the Current User's Information
----------------------------------

To get the current user, call [`client.user(user_id='me')`][user_init] to create the [`User`][user_class] object and
then call [`user.get(*, fields=None, headers=None, **kwargs)`][object_get] to retrieve the user information from the API.

<!-- sample get_users_me -->
```python
current_user = client.user().get()
```

[user_init]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.user

Create An Enterprise User
-------------------------

To create an enterprise user, call the [`client.create_user(name, login, **user_attributes)`][create_user] method.
This method returns a new [`User`][user_class] object.

<!-- sample post_users -->
```python
new_user = client.create_user('Temp User', 'user@example.com')
```

[create_user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_user

Get the Avatar for a User
-------------------------

To get the avatar for a user call the [`user.get_avatar()`][get_avatar] method with the [`User`][user_class] 
object for the user you wish to retrieve an avatar for. This will return the user avatar to you in bytes.

<!-- sample get_users_id_avatar -->
```python
avatar = client.user('33333').get_avatar()
```

[get_avatar]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.user.html#boxsdk.user.User.get_avatar

Create An App User
------------------

Custom applications may create App Users, which represent a "headless" user managed exclusively by the application.
These users can only be accessed via the API, and cannot login to the web application or other Box services.

To create a new app user, call [`client.create_user(name, login=None, **user_attributes)`][create_user] without a
`login` value.  This returns the [`User`][user_class] object for the new app user.

<!-- sample post_users_app -->
```python
new_app_user = client.create_user('App User 123', login=None)
```

Update User
-----------

To update a user object, call the [`user.update_info(data=data_to_update)`][update_info] method with a `dict` of fields to update
on the user.

<!-- sample put_users_id -->
```python
user_id = '33333'
user = client.user(user_id)
updated_user = user.update_info(data={'name': 'Smart User'})
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info

Delete User
-----------

To delete a user call the [`user.delete(notify=True, force=False)`][delete] method.  The method returns `True` to
indicate that the deletion succeeded.

The `notify` parameter determines whether the user should receive an email about the deletion,
and the `force` parameter will cause the user to be deleted even if they still have files in their account.  If `force`
is set to `False` and the user still has files in their account, the deletion will fail.

<!-- sample delete_users_id -->
```python
user_id = '33333'
client.user(user_id).delete(force=True)
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.delete

Invite User to Enterprise
-------------------------

To invite an existing user to join an Enterprise call the [`enterprise.invite_user(user_email)`][invite_user] method.  This
method returns an [`Invite`][invite_class] object representing the status of the invitation.

<!-- sample post_invites -->
```python
enterprise = client.get_current_enterprise()
invitation = enterprise.invite_user('user@example.com')
```

[invite_user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.enterprise.Enterprise.invite_user
[invite_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.invite.Invite

Get Email Aliases
-----------------

To get a user's email aliases call the [`user.get_email_aliases(limit=None, fields=None)`][get_email_aliases] method.
This method returns a [`BoxObjectCollection`][box_object_collection] used to iterate over the collection of
[`EmailAlias`][email_alias_class] objects.

<!-- sample get_users_id_email_aliases -->
```python
user_id = '33333'
user = client.user(user_id)
email_aliases = user.get_email_aliases()
for alias in email_aliases:
    print(f'User {user.id} has email alias {alias.email}')
```

[get_email_aliases]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.get_email_aliases
[box_object_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.pagination.box_object_collection.BoxObjectCollection
[email_alias_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.email_alias.EmailAlias

Add Email Alias
---------------

To add an email alias for a user, call the [`user.add_email_alias(email)`][add_email_alias] method with the email
address to add as an email alias for the user.  This will allow the user to log in and be collaborated by this email
in addition to their login email address. Not all emails addresses can be added as email aliases. Email addresses whose domains match the domain of the login email address can always be made aliases. Email addresses whose domains differ from the domain of the login email address can be made aliases depending on the Box account configuration. The method returns an [`EmailAlias`][email_alias_class] object. 

<!-- sample post_users_id_email_aliases -->
```python
user_id = '33333'
user = client.user(user_id)
email_alias = user.add_email_alias('alias@example.com')
```

[add_email_alias]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.add_email_alias

Remove Email Alias
------------------

To remove an email alias from a user, call the [`user.remove_email_alias(email_alias)`][remove_email_alias] method with
the [`EmailAlias`][email_alias_class] object to remove.  The method returns `True` to signify that the removal succeeded.

<!-- sample delete_users_id_email_aliases_id -->
```python
user_id = '33333'
email_alias_id = '12345'

user = client.user(user_id)
email_alias = client.email_alias(email_alias_id)

user.remove_email_alias(email_alias)
```

[remove_email_alias]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.remove_email_alias

Get Enterprise Users
--------------------

To get the users in an enterprise, call
[`client.users(limit=None, offset=0, filter_term=None, user_type=None, fields=None)`][get_users].  You can specify
a `filter_term` to filter on the user's `name` and `login` fields, or select a `user_type` to filter down to only
managed or external users.  This method returns a [`BoxObjectCollection`][box_object_collection] used to iterate over
the collection of [`User`][user_class] objects.

<!-- sample get_users -->
```python
users = client.users(user_type='all')
for user in users:
    print(f'{user.name} (User ID: {user.id})')
```

[get_users]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.users

Transfer User Content
---------------------

To move all of a user's content to a different user, call the
[`user.transfer_content(self, destination_user, notify=None, fields=None)`][transfer_content] method with the
[`User`][user_class] object representing the destination user.  This will create a new folder in the destination user's
account, containing all files and folders from the original user's account; the method returns a
[`Folder`][folder_class] object representing this new folder in the destination user's account.

<!-- sample put_users_id_folders_0 -->
```python
source_user_id = '33333'
destination_user_id = '44444'

user = client.user(source_user_id)
destination_user = client.user(destination_user_id)

folder = user.transfer_content(destination_user)
print(f'Created new folder "{folder.name}" in the account of user {destination_user.id}')
```

[transfer_content]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User.transfer_content
[folder_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder
