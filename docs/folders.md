# FoldersManager

- [Get folder information](#get-folder-information)
- [Update folder](#update-folder)
- [Delete folder](#delete-folder)
- [List items in folder](#list-items-in-folder)
- [Create folder](#create-folder)
- [Copy folder](#copy-folder)

## Get folder information

Retrieves details for a folder, including the first 100 entries
in the folder.

Passing `sort`, `direction`, `offset`, and `limit`
parameters in query allows you to manage the
list of returned
[folder items](https://developer.box.com/reference/resources/folder--full#param-item-collection).

To fetch more items within the folder, use the
[Get items in a folder](https://developer.box.com/reference/get-folders-id-items) endpoint.

This operation is performed by calling function `get_folder_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folders-id/).

<!-- sample get_folders_id -->

```python
client.folders.get_folder_by_id("0")
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested. Additionally this field can be used to query any metadata applied to the file by specifying the `metadata` field as well as the scope and key of the template to retrieve, for example `?fields=metadata.enterprise_12345.contractTemplate`.
- sort `Optional[GetFolderByIdSort]`
  - Defines the **second** attribute by which items are sorted. The folder type affects the way the items are sorted: _ **Standard folder**: Items are always sorted by their `type` first, with folders listed before files, and files listed before web links. _ **Root folder**: This parameter is not supported for marker-based pagination on the root folder (the folder with an `id` of `0`). \* **Shared folder with parent path to the associated folder visible to the collaborator**: Items are always sorted by their `type` first, with folders listed before files, and files listed before web links.
- direction `Optional[GetFolderByIdDirection]`
  - The direction to sort results in. This can be either in alphabetical ascending (`ASC`) or descending (`DESC`) order.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Offset-based pagination is not guaranteed to work reliably for high offset values and may fail for large datasets. In those cases, reduce the number of items in the folder (for example, by restructuring the folder into smaller subfolders) before retrying the request.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- if_none_match `Optional[str]`
  - Ensures an item is only returned if it has changed. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `304 Not Modified` if the item has not changed since.
- boxapi `Optional[str]`
  - The URL, and optional password, for the shared link of this item. This header can be used to access items that have not been explicitly shared with a user. Use the format `shared_link=[link]` or if a password is required then use `shared_link=[link]&shared_link_password=[password]`. This header can be used on the file or folder shared, as well as on any files or folders nested within the item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FolderFull`.

Returns a folder, including the first 100 entries in the folder.
If you used query parameters like
`sort`, `direction`, `offset`, or `limit`
the _folder items list_ will be affected accordingly.

To fetch more items within the folder, use the
[Get items in a folder](https://developer.box.com/reference/get-folders-id-items)) endpoint.

Not all available fields are returned by default. Use the
[fields](#parameter-fields) query parameter to explicitly request
any specific fields.

## Update folder

Updates a folder. This can be also be used to move the folder,
create shared links, update collaborations, and more.

This operation is performed by calling function `update_folder_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-folders-id/).

<!-- sample put_folders_id -->

```python
client.folders.update_folder_by_id(
    folder_to_update.id, name=updated_name, description="Updated description"
)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- name `Optional[str]`
  - The optional new name for this folder. The following restrictions to folder names apply: names containing non-printable ASCII characters, forward and backward slashes (`/`, `\`), names with trailing spaces, and names `.` and `..` are not allowed. Folder names must be unique within their parent folder. The name check is case-insensitive, so a folder named `New Folder` cannot be created in a parent folder that already contains a folder named `new folder`.
- description `Optional[str]`
  - The optional description of this folder.
- sync_state `Optional[UpdateFolderByIdSyncState]`
  - Specifies whether a folder should be synced to a user's device or not. This is used by Box Sync (discontinued) and is not used by Box Drive.
- can_non_owners_invite `Optional[bool]`
  - Specifies if users who are not the owner of the folder can invite new collaborators to the folder.
- parent `Optional[UpdateFolderByIdParent]`
- shared_link `Optional[UpdateFolderByIdSharedLink]`
- folder_upload_email `Optional[UpdateFolderByIdFolderUploadEmail]`
- tags `Optional[List[str]]`
  - The tags for this item. These tags are shown in the Box web app and mobile apps next to an item. To add or remove a tag, retrieve the item's current tags, modify them, and then update this field. There is a limit of 100 tags per item, and 10,000 unique tags per enterprise.
- is_collaboration_restricted_to_enterprise `Optional[bool]`
  - Specifies if new invites to this folder are restricted to users within the enterprise. This does not affect existing collaborations.
- collections `Optional[List[UpdateFolderByIdCollections]]`
  - An array of collections to make this folder a member of. Currently we only support the `favorites` collection. To get the ID for a collection, use the [List all collections][1] endpoint. Passing an empty array `[]` or `null` will remove the folder from all collections. [1]: https://developer.box.com/reference/get-collections
- can_non_owners_view_collaborators `Optional[bool]`
  - Restricts collaborators who are not the owner of this folder from viewing other collaborations on this folder. It also restricts non-owners from inviting new collaborators. When setting this field to `false`, it is required to also set `can_non_owners_invite_collaborators` to `false` if it has not already been set.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- if_match `Optional[str]`
  - Ensures this item hasn't recently changed before making changes. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `412 Precondition Failed` if it has changed since.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FolderFull`.

Returns a folder object for the updated folder

Not all available fields are returned by default. Use the
[fields](#parameter-fields) query parameter to explicitly request
any specific fields.

If the user is moving folders with a large number of items in all of
their descendants, the call will be run asynchronously. If the
operation is not completed within 10 minutes, the user will receive
a 200 OK response, and the operation will continue running.

## Delete folder

Deletes a folder, either permanently or by moving it to
the trash.

This operation is performed by calling function `delete_folder_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-folders-id/).

<!-- sample delete_folders_id -->

```python
client.folders.delete_folder_by_id(new_folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- recursive `Optional[bool]`
  - Delete a folder that is not empty by recursively deleting the folder and all of its content.
- if_match `Optional[str]`
  - Ensures this item hasn't recently changed before making changes. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `412 Precondition Failed` if it has changed since.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the folder is successfully deleted
or moved to the trash.

## List items in folder

Retrieves a page of items in a folder. These items can be files,
folders, and web links.

To request more information about the folder itself, like its size,
use the [Get a folder](https://developer.box.com/reference/get-folders-id) endpoint instead.

This operation is performed by calling function `get_folder_items`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folders-id-items/).

<!-- sample get_folders_id_items -->

```python
client.folders.get_folder_items(folder_origin.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested. Additionally this field can be used to query any metadata applied to the file by specifying the `metadata` field as well as the scope and key of the template to retrieve, for example `?fields=metadata.enterprise_12345.contractTemplate`.
- usemarker `Optional[bool]`
  - Specifies whether to use marker-based pagination instead of offset-based pagination. Only one pagination method can be used at a time. By setting this value to true, the API will return a `marker` field that can be passed as a parameter to this endpoint to get the next page of the response.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Offset-based pagination is not guaranteed to work reliably for high offset values and may fail for large datasets. In those cases, use marker-based pagination by setting `usemarker` to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- sort `Optional[GetFolderItemsSort]`
  - Defines the **second** attribute by which items are sorted. The folder type affects the way the items are sorted: _ **Standard folder**: Items are always sorted by their `type` first, with folders listed before files, and files listed before web links. _ **Root folder**: This parameter is not supported for marker-based pagination on the root folder (the folder with an `id` of `0`). \* **Shared folder with parent path to the associated folder visible to the collaborator**: Items are always sorted by their `type` first, with folders listed before files, and files listed before web links.
- direction `Optional[GetFolderItemsDirection]`
  - The direction to sort results in. This can be either in alphabetical ascending (`ASC`) or descending (`DESC`) order.
- boxapi `Optional[str]`
  - The URL, and optional password, for the shared link of this item. This header can be used to access items that have not been explicitly shared with a user. Use the format `shared_link=[link]` or if a password is required then use `shared_link=[link]&shared_link_password=[password]`. This header can be used on the file or folder shared, as well as on any files or folders nested within the item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Items`.

Returns a collection of files, folders, and web links contained in a folder.

## Create folder

Creates a new empty folder within the specified parent folder.

This operation is performed by calling function `create_folder`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-folders/).

<!-- sample post_folders -->

```python
client.folders.create_folder(new_folder_name, CreateFolderParent(id="0"))
```

### Arguments

- name `str`
  - The name for the new folder. The following restrictions to folder names apply: names containing non-printable ASCII characters, forward and backward slashes (`/`, `\`), names with trailing spaces, and names `.` and `..` are not allowed. Folder names must be unique within their parent folder. The name check is case-insensitive, so a folder named `New Folder` cannot be created in a parent folder that already contains a folder named `new folder`.
- parent `CreateFolderParent`
  - The parent folder to create the new folder within.
- folder_upload_email `Optional[CreateFolderFolderUploadEmail]`
- sync_state `Optional[CreateFolderSyncState]`
  - Specifies whether a folder should be synced to a user's device or not. This is used by Box Sync (discontinued) and is not used by Box Drive.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FolderFull`.

Returns a folder object.

Not all available fields are returned by default. Use the
[fields](#parameter-fields) query parameter to explicitly request
any specific fields.

## Copy folder

Creates a copy of a folder within a destination folder.

The original folder will not be changed.

This operation is performed by calling function `copy_folder`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-folders-id-copy/).

<!-- sample post_folders_id_copy -->

```python
client.folders.copy_folder(
    folder_origin.id, CopyFolderParent(id="0"), name=copied_folder_name
)
```

### Arguments

- folder_id `str`
  - The unique identifier of the folder to copy. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder with the ID `0` can not be copied. Example: "0"
- name `Optional[str]`
  - An optional new name for the copied folder. There are some restrictions to the file name. Names containing non-printable ASCII characters, forward and backward slashes (`/`, `\`), as well as names with trailing spaces are prohibited. Additionally, the names `.` and `..` are not allowed either.
- parent `CopyFolderParent`
  - The destination folder to copy the folder to.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FolderFull`.

Returns a new folder object representing the copied folder.

Not all available fields are returned by default. Use the
[fields](#parameter-fields) query parameter to explicitly request
any specific fields.
