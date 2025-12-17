# TrashedFilesManager

- [Restore file](#restore-file)
- [Get trashed file](#get-trashed-file)
- [Permanently remove file](#permanently-remove-file)

## Restore file

Restores a file that has been moved to the trash.

An optional new parent ID can be provided to restore the file to in case the
original folder has been deleted.

This operation is performed by calling function `restore_file_from_trash`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-files-id/).

<!-- sample post_files_id -->

```python
client.trashed_files.restore_file_from_trash(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- name `Optional[str]`
  - An optional new name for the file.
- parent `Optional[RestoreFileFromTrashParent]`
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TrashFileRestored`.

Returns a file object when the file has been restored.

## Get trashed file

Retrieves a file that has been moved to the trash.

Please note that only if the file itself has been moved to the
trash can it be retrieved with this API call. If instead one of
its parent folders was moved to the trash, only that folder
can be inspected using the
[`GET /folders/:id/trash`](https://developer.box.com/reference/get-folders-id-trash) API.

To list all items that have been moved to the trash, please
use the [`GET /folders/trash/items`](https://developer.box.com/reference/get-folders-trash-items/)
API.

This operation is performed by calling function `get_trashed_file_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-trash/).

<!-- sample get_files_id_trash -->

```python
client.trashed_files.get_trashed_file_by_id(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TrashFile`.

Returns the file that was trashed,
including information about when the it
was moved to the trash.

## Permanently remove file

Permanently deletes a file that is in the trash.
This action cannot be undone.

This operation is performed by calling function `delete_trashed_file_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-files-id-trash/).

<!-- sample delete_files_id_trash -->

```python
client.trashed_files.delete_trashed_file_by_id(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the file was
permanently deleted.
