# TrashedFoldersManager

- [Restore folder](#restore-folder)
- [Get trashed folder](#get-trashed-folder)
- [Permanently remove folder](#permanently-remove-folder)

## Restore folder

Restores a folder that has been moved to the trash.

An optional new parent ID can be provided to restore the folder to in case the
original folder has been deleted.

During this operation, part of the file tree will be locked, mainly
the source folder and all of its descendants, as well as the destination
folder.

For the duration of the operation, no other move, copy, delete, or restore
operation can performed on any of the locked folders.

This operation is performed by calling function `restore_folder_from_trash`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-folders-id/).

<!-- sample post_folders_id -->

```python
client.trashed_folders.restore_folder_from_trash(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- name `Optional[str]`
  - An optional new name for the folder.
- parent `Optional[RestoreFolderFromTrashParent]`
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TrashFolderRestored`.

Returns a folder object when the folder has been restored.

## Get trashed folder

Retrieves a folder that has been moved to the trash.

Please note that only if the folder itself has been moved to the
trash can it be retrieved with this API call. If instead one of
its parent folders was moved to the trash, only that folder
can be inspected using the
[`GET /folders/:id/trash`](e://get_folders_id_trash) API.

To list all items that have been moved to the trash, please
use the [`GET /folders/trash/items`](e://get-folders-trash-items/)
API.

This operation is performed by calling function `get_trashed_folder_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folders-id-trash/).

<!-- sample get_folders_id_trash -->

```python
client.trashed_folders.get_trashed_folder_by_id(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TrashFolder`.

Returns the folder that was trashed,
including information about when the it
was moved to the trash.

## Permanently remove folder

Permanently deletes a folder that is in the trash.
This action cannot be undone.

This operation is performed by calling function `delete_trashed_folder_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-folders-id-trash/).

<!-- sample delete_folders_id_trash -->

```python
client.trashed_folders.delete_trashed_folder_by_id(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the folder was
permanently deleted.
