# TransferManager

- [Transfer owned folders](#transfer-owned-folders)

## Transfer owned folders

Move all of the items (files, folders and workflows) owned by a user into
another user's account

Only the root folder (`0`) can be transferred.

Folders can only be moved across users by users with administrative
permissions.

All existing shared links and folder-level collaborations are transferred
during the operation. Please note that while collaborations at the individual
file-level are transferred during the operation, the collaborations are
deleted when the original user is deleted.

If the user has a large number of items across all folders, the call will
be run asynchronously. If the operation is not completed within 10 minutes,
the user will receive a 200 OK response, and the operation will continue running.

If the destination path has a metadata cascade policy attached to any of
the parent folders, a metadata cascade operation will be kicked off
asynchronously.

There is currently no way to check for when this operation is finished.

The destination folder's name will be in the format `{User}'s Files and
Folders`, where `{User}` is the display name of the user.

To make this API call your application will need to have the "Read and write
all files and folders stored in Box" scope enabled.

Please make sure the destination user has access to `Relay` or `Relay Lite`,
and has access to the files and folders involved in the workflows being
transferred.

Admins will receive an email when the operation is completed.

This operation is performed by calling function `transfer_owned_folder`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-users-id-folders-0/).

<!-- sample put_users_id_folders_0 -->

```python
client.transfer.transfer_owned_folder(source_user.id, TransferOwnedFolderOwnedBy(id=target_user.id), notify=False)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- owned_by `TransferOwnedFolderOwnedBy`
  - The user who the folder will be transferred to.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- notify `Optional[bool]`
  - Determines if users should receive email notification for the action performed.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FolderFull`.

Returns the information for the newly created
destination folder.
