# UsersManager

- [List enterprise users](#list-enterprise-users)
- [Create user](#create-user)
- [Get current user](#get-current-user)
- [Get user](#get-user)
- [Update user](#update-user)
- [Delete user](#delete-user)

## List enterprise users

Returns a list of all users for the Enterprise along with their `user_id`,
`public_name`, and `login`.

The application and the authenticated user need to
have the permission to look up users in the entire
enterprise.

This operation is performed by calling function `get_users`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-users/).

<!-- sample get_users -->

```python
client.users.get_users()
```

### Arguments

- filter_term `Optional[str]`
  - Limits the results to only users who's `name` or `login` start with the search term. For externally managed users, the search term needs to completely match the in order to find the user, and it will only return one user at a time.
- user_type `Optional[GetUsersUserType]`
  - Limits the results to the kind of user specified. _ `all` returns every kind of user for whom the `login` or `name` partially matches the `filter_term`. It will only return an external user if the login matches the `filter_term` completely, and in that case it will only return that user. _ `managed` returns all managed and app users for whom the `login` or `name` partially matches the `filter_term`. \* `external` returns all external users for whom the `login` matches the `filter_term` exactly.
- external_app_user_id `Optional[str]`
  - Limits the results to app users with the given `external_app_user_id` value. When creating an app user, an `external_app_user_id` value can be set. This value can then be used in this endpoint to find any users that match that `external_app_user_id` value.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- usemarker `Optional[bool]`
  - Specifies whether to use marker-based pagination instead of offset-based pagination. Only one pagination method can be used at a time. By setting this value to true, the API will return a `marker` field that can be passed as a parameter to this endpoint to get the next page of the response.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Users`.

Returns all of the users in the enterprise.

## Create user

Creates a new managed user in an enterprise. This endpoint
is only available to users and applications with the right
admin permissions.

This operation is performed by calling function `create_user`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-users/).

<!-- sample post_users -->

```python
client.users.create_user(user_name, login=user_login, is_platform_access_only=True)
```

### Arguments

- name `str`
  - The name of the user.
- login `Optional[str]`
  - The email address the user uses to log in Required, unless `is_platform_access_only` is set to `true`.
- is_platform_access_only `Optional[bool]`
  - Specifies that the user is an app user.
- role `Optional[CreateUserRole]`
  - The user’s enterprise role.
- language `Optional[str]`
  - The language of the user, formatted in modified version of the [ISO 639-1](/guides/api-calls/language-codes) format.
- is_sync_enabled `Optional[bool]`
  - Whether the user can use Box Sync.
- job_title `Optional[str]`
  - The user’s job title.
- phone `Optional[str]`
  - The user’s phone number.
- address `Optional[str]`
  - The user’s address.
- space_amount `Optional[int]`
  - The user’s total available space in bytes. Set this to `-1` to indicate unlimited storage.
- tracking_codes `Optional[List[TrackingCode]]`
  - Tracking codes allow an admin to generate reports from the admin console and assign an attribute to a specific group of users. This setting must be enabled for an enterprise before it can be used.
- can_see_managed_users `Optional[bool]`
  - Whether the user can see other enterprise users in their contact list.
- timezone `Optional[str]`
  - The user's timezone.
- is_external_collab_restricted `Optional[bool]`
  - Whether the user is allowed to collaborate with users outside their enterprise.
- is_exempt_from_device_limits `Optional[bool]`
  - Whether to exempt the user from enterprise device limits.
- is_exempt_from_login_verification `Optional[bool]`
  - Whether the user must use two-factor authentication.
- status `Optional[CreateUserStatus]`
  - The user's account status.
- external_app_user_id `Optional[str]`
  - An external identifier for an app user, which can be used to look up the user. This can be used to tie user IDs from external identity providers to Box users.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `UserFull`.

Returns a user object for the newly created user.

## Get current user

Retrieves information about the user who is currently authenticated.

In the case of a client-side authenticated OAuth 2.0 application
this will be the user who authorized the app.

In the case of a JWT, server-side authenticated application
this will be the service account that belongs to the application
by default.

Use the `As-User` header to change who this API call is made on behalf of.

This operation is performed by calling function `get_user_me`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-users-me/).

<!-- sample get_users_me -->

```python
client.users.get_user_me()
```

### Arguments

- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `UserFull`.

Returns a single user object.

## Get user

Retrieves information about a user in the enterprise.

The application and the authenticated user need to
have the permission to look up users in the entire
enterprise.

This endpoint also returns a limited set of information
for external users who are collaborated on content
owned by the enterprise for authenticated users with the
right scopes. In this case, disallowed fields will return
null instead.

This operation is performed by calling function `get_user_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-users-id/).

<!-- sample get_users_id -->

```python
client.users.get_user_by_id(user.id)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `UserFull`.

Returns a single user object.

Not all available fields are returned by default. Use the
[fields](#param-fields) query parameter to explicitly request
any specific fields using the [fields](#get-users-id--request--fields)
parameter.

## Update user

Updates a managed or app user in an enterprise. This endpoint
is only available to users and applications with the right
admin permissions.

This operation is performed by calling function `update_user_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-users-id/).

<!-- sample put_users_id -->

```python
client.users.update_user_by_id(user.id, name=updated_user_name)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- enterprise `Optional[str]`
  - Set this to `null` to roll the user out of the enterprise and make them a free user.
- notify `Optional[bool]`
  - Whether the user should receive an email when they are rolled out of an enterprise.
- name `Optional[str]`
  - The name of the user.
- login `Optional[str]`
  - The email address the user uses to log in Note: If the target user's email is not confirmed, then the primary login address cannot be changed.
- role `Optional[UpdateUserByIdRole]`
  - The user’s enterprise role.
- language `Optional[str]`
  - The language of the user, formatted in modified version of the [ISO 639-1](/guides/api-calls/language-codes) format.
- is_sync_enabled `Optional[bool]`
  - Whether the user can use Box Sync.
- job_title `Optional[str]`
  - The user’s job title.
- phone `Optional[str]`
  - The user’s phone number.
- address `Optional[str]`
  - The user’s address.
- tracking_codes `Optional[List[TrackingCode]]`
  - Tracking codes allow an admin to generate reports from the admin console and assign an attribute to a specific group of users. This setting must be enabled for an enterprise before it can be used.
- can_see_managed_users `Optional[bool]`
  - Whether the user can see other enterprise users in their contact list.
- timezone `Optional[str]`
  - The user's timezone.
- is_external_collab_restricted `Optional[bool]`
  - Whether the user is allowed to collaborate with users outside their enterprise.
- is_exempt_from_device_limits `Optional[bool]`
  - Whether to exempt the user from enterprise device limits.
- is_exempt_from_login_verification `Optional[bool]`
  - Whether the user must use two-factor authentication.
- is_password_reset_required `Optional[bool]`
  - Whether the user is required to reset their password.
- status `Optional[UpdateUserByIdStatus]`
  - The user's account status.
- space_amount `Optional[int]`
  - The user’s total available space in bytes. Set this to `-1` to indicate unlimited storage.
- notification_email `Optional[UpdateUserByIdNotificationEmail]`
  - An alternate notification email address to which email notifications are sent. When it's confirmed, this will be the email address to which notifications are sent instead of to the primary email address. Set this value to `null` to remove the notification email.
- external_app_user_id `Optional[str]`
  - An external identifier for an app user, which can be used to look up the user. This can be used to tie user IDs from external identity providers to Box users. Note: In order to update this field, you need to request a token using the application that created the app user.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `UserFull`.

Returns the updated user object.

## Delete user

Deletes a user. By default this will fail if the user
still owns any content. Move their owned content first
before proceeding, or use the `force` field to delete
the user and their files.

This operation is performed by calling function `delete_user_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-users-id/).

<!-- sample delete_users_id -->

```python
client.users.delete_user_by_id(user.id)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- notify `Optional[bool]`
  - Whether the user will receive email notification of the deletion.
- force `Optional[bool]`
  - Whether the user should be deleted even if this user still own files.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Removes the user and returns an empty response.
