# FolderLocksManager

- [List folder locks](#list-folder-locks)
- [Create folder lock](#create-folder-lock)
- [Delete folder lock](#delete-folder-lock)

## List folder locks

Retrieves folder lock details for a given folder.

You must be authenticated as the owner or co-owner of the folder to
use this endpoint.

This operation is performed by calling function `get_folder_locks`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folder-locks/).

<!-- sample get_folder_locks -->

```python
client.folder_locks.get_folder_locks(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FolderLocks`.

Returns details for all folder locks applied to the folder, including the
lock type and user that applied the lock.

## Create folder lock

Creates a folder lock on a folder, preventing it from being moved and/or
deleted.

You must be authenticated as the owner or co-owner of the folder to
use this endpoint.

This operation is performed by calling function `create_folder_lock`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-folder-locks/).

<!-- sample post_folder_locks -->

```python
client.folder_locks.create_folder_lock(CreateFolderLockFolder(id=folder.id, type='folder'), locked_operations=CreateFolderLockLockedOperations(move=True, delete=True))
```

### Arguments

- locked_operations `Optional[CreateFolderLockLockedOperations]`
  - The operations to lock for the folder. If `locked_operations` is included in the request, both `move` and `delete` must also be included and both set to `true`.
- folder `CreateFolderLockFolder`
  - The folder to apply the lock to.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FolderLock`.

Returns the instance of the folder lock that was applied to the folder,
including the user that applied the lock and the operations set.

## Delete folder lock

Deletes a folder lock on a given folder.

You must be authenticated as the owner or co-owner of the folder to
use this endpoint.

This operation is performed by calling function `delete_folder_lock_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-folder-locks-id/).

<!-- sample delete_folder_locks_id -->

```python
client.folder_locks.delete_folder_lock_by_id(folder_lock.id)
```

### Arguments

- folder_lock_id `str`
  - The ID of the folder lock. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the folder lock is successfully deleted.
