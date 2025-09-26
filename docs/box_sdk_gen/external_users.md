# ExternalUsersManager

- [Submit job to delete external users](#submit-job-to-delete-external-users)

## Submit job to delete external users

Delete external users from current user enterprise. This will remove each
external user from all invited collaborations within the current enterprise.

This operation is performed by calling function `submit_job_to_delete_external_users_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-external-users-submit-delete-job/).

<!-- sample post_external_users_submit_delete_job_v2025.0 -->

```python
client.external_users.submit_job_to_delete_external_users_v2025_r0([UserReferenceV2025R0(id=get_env_var('BOX_EXTERNAL_USER_ID'))])
```

### Arguments

- external_users `List[UserReferenceV2025R0]`
  - List of external users to delete.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ExternalUsersSubmitDeleteJobResponseV2025R0`.
