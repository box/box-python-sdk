# TermsOfServiceUserStatusesManager

- [List terms of service user statuses](#list-terms-of-service-user-statuses)
- [Create terms of service status for new user](#create-terms-of-service-status-for-new-user)
- [Update terms of service status for existing user](#update-terms-of-service-status-for-existing-user)

## List terms of service user statuses

Retrieves an overview of users and their status for a
terms of service, including Whether they have accepted
the terms and when.

This operation is performed by calling function `get_terms_of_service_user_statuses`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-terms-of-service-user-statuses/).

<!-- sample get_terms_of_service_user_statuses -->

```python
client.terms_of_service_user_statuses.get_terms_of_service_user_statuses(
    tos.id, user_id=user.id
)
```

### Arguments

- tos_id `str`
  - The ID of the terms of service.
- user_id `Optional[str]`
  - Limits results to the given user ID.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TermsOfServiceUserStatuses`.

Returns a list of terms of service statuses.

## Create terms of service status for new user

Sets the status for a terms of service for a user.

This operation is performed by calling function `create_terms_of_service_status_for_user`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-terms-of-service-user-statuses/).

<!-- sample post_terms_of_service_user_statuses -->

```python
client.terms_of_service_user_statuses.create_terms_of_service_status_for_user(
    CreateTermsOfServiceStatusForUserTos(id=tos.id),
    CreateTermsOfServiceStatusForUserUser(id=user.id),
    False,
)
```

### Arguments

- tos `CreateTermsOfServiceStatusForUserTos`
  - The terms of service to set the status for.
- user `CreateTermsOfServiceStatusForUserUser`
  - The user to set the status for.
- is_accepted `bool`
  - Whether the user has accepted the terms.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TermsOfServiceUserStatus`.

Returns a terms of service status object.

## Update terms of service status for existing user

Updates the status for a terms of service for a user.

This operation is performed by calling function `update_terms_of_service_status_for_user_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-terms-of-service-user-statuses-id/).

<!-- sample put_terms_of_service_user_statuses_id -->

```python
client.terms_of_service_user_statuses.update_terms_of_service_status_for_user_by_id(
    created_tos_user_status.id, True
)
```

### Arguments

- terms_of_service_user_status_id `str`
  - The ID of the terms of service status. Example: "324234"
- is_accepted `bool`
  - Whether the user has accepted the terms.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TermsOfServiceUserStatus`.

Returns the updated terms of service status object.
