# ListCollaborationsManager

- [List file collaborations](#list-file-collaborations)
- [List folder collaborations](#list-folder-collaborations)
- [List pending collaborations](#list-pending-collaborations)
- [List group collaborations](#list-group-collaborations)

## List file collaborations

Retrieves a list of pending and active collaborations for a
file. This returns all the users that have access to the file
or have been invited to the file.

This operation is performed by calling function `get_file_collaborations`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-collaborations/).

<!-- sample get_files_id_collaborations -->

```python
client.list_collaborations.get_file_collaborations(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Collaborations`.

Returns a collection of collaboration objects. If there are no
collaborations on this file an empty collection will be returned.

This list includes pending collaborations, for which the `status`
is set to `pending`, indicating invitations that have been sent but not
yet accepted.

## List folder collaborations

Retrieves a list of pending and active collaborations for a
folder. This returns all the users that have access to the folder
or have been invited to the folder.

This operation is performed by calling function `get_folder_collaborations`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folders-id-collaborations/).

<!-- sample get_folders_id_collaborations -->

```python
client.list_collaborations.get_folder_collaborations(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Collaborations`.

Returns a collection of collaboration objects. If there are no
collaborations on this folder an empty collection will be returned.

This list includes pending collaborations, for which the `status`
is set to `pending`, indicating invitations that have been sent but not
yet accepted.

## List pending collaborations

Retrieves all pending collaboration invites for this user.

This operation is performed by calling function `get_collaborations`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collaborations/).

<!-- sample get_collaborations -->

```python
client.list_collaborations.get_collaborations(GetCollaborationsStatus.PENDING)
```

### Arguments

- status `GetCollaborationsStatus`
  - The status of the collaborations to retrieve.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationsOffsetPaginated`.

Returns a collection of pending collaboration objects.

If the user has no pending collaborations, the collection
will be empty.

## List group collaborations

Retrieves all the collaborations for a group. The user
must have admin permissions to inspect enterprise's groups.

Each collaboration object has details on which files or
folders the group has access to and with what role.

This operation is performed by calling function `get_group_collaborations`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-groups-id-collaborations/).

<!-- sample get_groups_id_collaborations -->

```python
client.list_collaborations.get_group_collaborations(group.id)
```

### Arguments

- group_id `str`
  - The ID of the group. Example: "57645"
- limit `Optional[int]`
  - The maximum number of items to return per page.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `CollaborationsOffsetPaginated`.

Returns a collection of collaboration objects. If there are no
collaborations, an empty collection will be returned.
