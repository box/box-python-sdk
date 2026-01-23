# FileVersionsManager

- [List all file versions](#list-all-file-versions)
- [Get file version](#get-file-version)
- [Remove file version](#remove-file-version)
- [Restore file version](#restore-file-version)
- [Promote file version](#promote-file-version)

## List all file versions

Retrieve a list of the past versions for a file.

Versions are only tracked by Box users with premium accounts. To fetch the ID
of the current version of a file, use the `GET /file/:id` API.

This operation is performed by calling function `get_file_versions`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-versions/).

<!-- sample get_files_id_versions -->

```python
client.file_versions.get_file_versions(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileVersions`.

Returns an array of past versions for this file.

## Get file version

Retrieve a specific version of a file.

Versions are only tracked for Box users with premium accounts.

This operation is performed by calling function `get_file_version_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-versions-id/).

<!-- sample get_files_id_versions_id -->

```python
client.file_versions.get_file_version_by_id(file.id, file_versions.entries[0].id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- file_version_id `str`
  - The ID of the file version. Example: "1234"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileVersionFull`.

Returns a specific version of a file.

Not all available fields are returned by default. Use the
[fields](#parameter-fields) query parameter to explicitly request
any specific fields.

## Remove file version

Move a file version to the trash.

Versions are only tracked for Box users with premium accounts.

This operation is performed by calling function `delete_file_version_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-files-id-versions-id/).

<!-- sample delete_files_id_versions_id -->

```python
client.file_versions.delete_file_version_by_id(file.id, file_version.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- file_version_id `str`
  - The ID of the file version. Example: "1234"
- if_match `Optional[str]`
  - Ensures this item hasn't recently changed before making changes. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `412 Precondition Failed` if it has changed since.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the file has been successfully
deleted.

## Restore file version

Restores a specific version of a file after it was deleted.
Don't use this endpoint to restore Box Notes,
as it works with file formats such as PDF, DOC,
PPTX or similar.

This operation is performed by calling function `update_file_version_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-files-id-versions-id/).

<!-- sample put_files_id_versions_id -->

```python
client.file_versions.update_file_version_by_id(
    file.id, file_version.id, trashed_at=create_null()
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- file_version_id `str`
  - The ID of the file version. Example: "1234"
- trashed_at `Optional[str]`
  - Set this to `null` to clear the date and restore the file.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileVersionFull`.

Returns a restored file version object.

## Promote file version

Promote a specific version of a file.

If previous versions exist, this method can be used to
promote one of the older versions to the top of the version history.

This creates a new copy of the old version and puts it at the
top of the versions history. The file will have the exact same contents
as the older version, with the same hash digest, `etag`, and
name as the original.

Other properties such as comments do not get updated to their
former values.

Don't use this endpoint to restore Box Notes,
as it works with file formats such as PDF, DOC,
PPTX or similar.

This operation is performed by calling function `promote_file_version`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-files-id-versions-current/).

<!-- sample post_files_id_versions_current -->

```python
client.file_versions.promote_file_version(
    file.id, id=file_versions.entries[0].id, type=PromoteFileVersionType.FILE_VERSION
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- id `Optional[str]`
  - The file version ID.
- type `Optional[PromoteFileVersionType]`
  - The type to promote.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileVersionFull`.

Returns a newly created file version object.
