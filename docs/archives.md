# ArchivesManager

- [List archives](#list-archives)
- [Create archive](#create-archive)
- [Delete archive](#delete-archive)

## List archives

Retrieves archives for an enterprise.

This operation is performed by calling function `get_archives_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-archives/).

<!-- sample get_archives_v2025.0 -->

```python
client.archives.get_archives_v2025_r0(limit=100)
```

### Arguments

- limit `Optional[int]`
  - The maximum number of items to return per page.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ArchivesV2025R0`.

Returns a list of archives in the enterprise.

## Create archive

Creates an archive.

This operation is performed by calling function `create_archive_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-archives/).

<!-- sample post_archives_v2025.0 -->

```python
client.archives.create_archive_v2025_r0(archive_name)
```

### Arguments

- name `str`
  - The name of the archive.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ArchiveV2025R0`.

Returns a new archive object.

## Delete archive

Permanently deletes an archive.

This operation is performed by calling function `delete_archive_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/delete-archives-id/).

<!-- sample delete_archives_id_v2025.0 -->

```python
client.archives.delete_archive_by_id_v2025_r0(archive.id)
```

### Arguments

- archive_id `str`
  - The ID of the archive. Example: "982312"
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the archive has been deleted.
