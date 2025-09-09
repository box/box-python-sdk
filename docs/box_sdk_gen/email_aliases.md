# EmailAliasesManager

- [List user's email aliases](#list-users-email-aliases)
- [Create email alias](#create-email-alias)
- [Remove email alias](#remove-email-alias)

## List user's email aliases

Retrieves all email aliases for a user. The collection
does not include the primary login for the user.

This operation is performed by calling function `get_user_email_aliases`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-users-id-email-aliases/).

<!-- sample get_users_id_email_aliases -->

```python
client.email_aliases.get_user_email_aliases(new_user.id)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `EmailAliases`.

Returns a collection of email aliases.

## Create email alias

Adds a new email alias to a user account..

This operation is performed by calling function `create_user_email_alias`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-users-id-email-aliases/).

<!-- sample post_users_id_email_aliases -->

```python
client.email_aliases.create_user_email_alias(new_user.id, new_alias_email)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- email `str`
  - The email address to add to the account as an alias. Note: The domain of the email alias needs to be registered to your enterprise. See the [domain verification guide](https://support.box.com/hc/en-us/articles/4408619650579-Domain-Verification) for steps to add a new domain.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `EmailAlias`.

Returns the newly created email alias object.

## Remove email alias

Removes an email alias from a user.

This operation is performed by calling function `delete_user_email_alias_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-users-id-email-aliases-id/).

<!-- sample delete_users_id_email_aliases_id -->

```python
client.email_aliases.delete_user_email_alias_by_id(new_user.id, new_alias.id)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- email_alias_id `str`
  - The ID of the email alias. Example: "23432"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Removes the alias and returns an empty response.
