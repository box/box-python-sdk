# ExternalUsersManager

- [Submit job to delete external users](#submit-job-to-delete-external-users)

## Submit job to delete external users

Delete external users from current user enterprise. This will remove each
external user from all invited collaborations within the current enterprise.

This operation is performed by calling function `create_external_user_submit_delete_job_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-external-users-submit-delete-job/).

_Currently we don't have an example for calling `create_external_user_submit_delete_job_v2025_r0` in integration tests_

### Arguments

- external_users `List[UserReferenceV2025R0]`
  - List of external users to delete.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ExternalUsersSubmitDeleteJobResponseV2025R0`.
