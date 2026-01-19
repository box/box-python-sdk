# ArchivesManager

- [List archives](#list-archives)
- [Create archive](#create-archive)
- [Delete archive](#delete-archive)
- [Update archive](#update-archive)

## List archives

Retrieves archives for an enterprise.

To learn more about the archive APIs, see the [Archive API Guide](https://developer.box.com/guides/archives).

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

To learn more about the archive APIs, see the [Archive API Guide](https://developer.box.com/guides/archives).

This operation is performed by calling function `create_archive_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-archives/).

<!-- sample post_archives_v2025.0 -->

```python
client.archives.create_archive_v2025_r0(archive_name, description=archive_description)
```

### Arguments

- name `str`
  - The name of the archive.
- description `Optional[str]`
  - The description of the archive.
- storage_policy_id `Optional[str]`
  - The ID of the storage policy that the archive is assigned to.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ArchiveV2025R0`.

Returns a new archive object.

## Delete archive

Permanently deletes an archive.

To learn more about the archive APIs, see the [Archive API Guide](https://developer.box.com/guides/archives).

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

## Update archive

Updates an archive.

To learn more about the archive APIs, see the [Archive API Guide](https://developer.box.com/guides/archives).

This operation is performed by calling function `update_archive_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/put-archives-id/).

<!-- sample put_archives_id_v2025.0 -->

```python
client.archives.update_archive_by_id_v2025_r0(archive.id, name=new_archive_name, description=new_archive_description)
```

### Arguments

- archive_id `str`
  - The ID of the archive. Example: "982312"
- name `Optional[str]`
  - The name of the archive.
- description `Optional[str]`
  - The description of the archive.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ArchiveV2025R0`.

Returns the updated archive object.
