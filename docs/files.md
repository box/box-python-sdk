# FilesManager

- [Get file information](#get-file-information)
- [Update file](#update-file)
- [Delete file](#delete-file)
- [Copy file](#copy-file)
- [Get file thumbnail URL](#get-file-thumbnail-url)
- [Get file thumbnail](#get-file-thumbnail)

## Get file information

Retrieves the details about a file.

This operation is performed by calling function `get_file_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id/).

<!-- sample get_files_id -->

```python
client.files.get_file_by_id(
    uploaded_file.id, fields=["is_externally_owned", "has_collaborations"]
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested. Additionally this field can be used to query any metadata applied to the file by specifying the `metadata` field as well as the scope and key of the template to retrieve, for example `?fields=metadata.enterprise_12345.contractTemplate`.
- if_none_match `Optional[str]`
  - Ensures an item is only returned if it has changed. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `304 Not Modified` if the item has not changed since.
- boxapi `Optional[str]`
  - The URL, and optional password, for the shared link of this item. This header can be used to access items that have not been explicitly shared with a user. Use the format `shared_link=[link]` or if a password is required then use `shared_link=[link]&shared_link_password=[password]`. This header can be used on the file or folder shared, as well as on any files or folders nested within the item.
- x_rep_hints `Optional[str]`
  - A header required to request specific `representations` of a file. Use this in combination with the `fields` query parameter to request a specific file representation. The general format for these representations is `X-Rep-Hints: [...]` where `[...]` is one or many hints in the format `[fileType?query]`. For example, to request a `png` representation in `32x32` as well as `64x64` pixel dimensions provide the following hints. `x-rep-hints: [jpg?dimensions=32x32][jpg?dimensions=64x64]` Additionally, a `text` representation is available for all document file types in Box using the `[extracted_text]` representation. `x-rep-hints: [extracted_text]`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns a file object.

Not all available fields are returned by default. Use the
[fields](#param-fields) query parameter to explicitly request
any specific fields.

## Update file

Updates a file. This can be used to rename or move a file,
create a shared link, or lock a file.

This operation is performed by calling function `update_file_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-files-id/).

<!-- sample put_files_id -->

```python
client.files.update_file_by_id(
    file_to_update.id, name=updated_name, description="Updated description"
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- name `Optional[str]`
  - An optional different name for the file. This can be used to rename the file. File names must be unique within their parent folder. The name check is case-insensitive, so a file named `New File` cannot be created in a parent folder that already contains a folder named `new file`.
- description `Optional[str]`
  - The description for a file. This can be seen in the right-hand sidebar panel when viewing a file in the Box web app. Additionally, this index is used in the search index of the file, allowing users to find the file by the content in the description.
- parent `Optional[UpdateFileByIdParent]`
- shared_link `Optional[UpdateFileByIdSharedLink]`
- lock `Optional[UpdateFileByIdLock]`
  - Defines a lock on an item. This prevents the item from being moved, renamed, or otherwise changed by anyone other than the user who created the lock. Set this to `null` to remove the lock.
- disposition_at `Optional[DateTime]`
  - The retention expiration timestamp for the given file. This date cannot be shortened once set on a file.
- permissions `Optional[UpdateFileByIdPermissions]`
  - Defines who can download a file.
- collections `Optional[List[UpdateFileByIdCollections]]`
  - An array of collections to make this file a member of. Currently we only support the `favorites` collection. To get the ID for a collection, use the [List all collections][1] endpoint. Passing an empty array `[]` or `null` will remove the file from all collections. [1]: https://developer.box.com/reference/get-collections
- tags `Optional[List[str]]`
  - The tags for this item. These tags are shown in the Box web app and mobile apps next to an item. To add or remove a tag, retrieve the item's current tags, modify them, and then update this field. There is a limit of 100 tags per item, and 10,000 unique tags per enterprise.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- if_match `Optional[str]`
  - Ensures this item hasn't recently changed before making changes. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `412 Precondition Failed` if it has changed since.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns a file object.

Not all available fields are returned by default. Use the
[fields](#param-fields) query parameter to explicitly request
any specific fields.

## Delete file

Deletes a file, either permanently or by moving it to
the trash.

The enterprise settings determine whether the item will
be permanently deleted from Box or moved to the trash.

This operation is performed by calling function `delete_file_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-files-id/).

<!-- sample delete_files_id -->

```python
client.files.delete_file_by_id(thumbnail_file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- if_match `Optional[str]`
  - Ensures this item hasn't recently changed before making changes. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `412 Precondition Failed` if it has changed since.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the file has been successfully
deleted.

## Copy file

Creates a copy of a file.

This operation is performed by calling function `copy_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-files-id-copy/).

<!-- sample post_files_id_copy -->

```python
client.files.copy_file(file_origin.id, CopyFileParent(id="0"), name=copied_file_name)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- name `Optional[str]`
  - An optional new name for the copied file. There are some restrictions to the file name. Names containing non-printable ASCII characters, forward and backward slashes (`/`, `\`), and protected names like `.` and `..` are automatically sanitized by removing the non-allowed characters.
- version `Optional[str]`
  - An optional ID of the specific file version to copy.
- parent `CopyFileParent`
  - The destination folder to copy the file to.
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns a new file object representing the copied file.

Not all available fields are returned by default. Use the
[fields](#param-fields) query parameter to explicitly request
any specific fields.

## Get file thumbnail URL

Get the download URL without downloading the content.

This operation is performed by calling function `get_file_thumbnail_url`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-thumbnail-id/).

<!-- sample get_files_id_thumbnail_id -->

```python
client.files.get_file_thumbnail_url(thumbnail_file.id, GetFileThumbnailUrlExtension.PNG)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- extension `GetFileThumbnailUrlExtension`
  - The file format for the thumbnail. Example: "png"
- min_height `Optional[int]`
  - The minimum height of the thumbnail.
- min_width `Optional[int]`
  - The minimum width of the thumbnail.
- max_height `Optional[int]`
  - The maximum height of the thumbnail.
- max_width `Optional[int]`
  - The maximum width of the thumbnail.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `str`.

When a thumbnail can be created the thumbnail data will be
returned in the body of the response.Sometimes generating a thumbnail can take a few seconds. In these
situations the API returns a `Location`-header pointing to a
placeholder graphic for this file type.

The placeholder graphic can be used in a user interface until the
thumbnail generation has completed. The `Retry-After`-header indicates
when to the thumbnail will be ready. At that time, retry this endpoint
to retrieve the thumbnail.

## Get file thumbnail

Retrieves a thumbnail, or smaller image representation, of a file.

Sizes of `32x32`,`64x64`, `128x128`, and `256x256` can be returned in
the `.png` format and sizes of `32x32`, `160x160`, and `320x320`
can be returned in the `.jpg` format.

Thumbnails can be generated for the image and video file formats listed
[found on our community site][1].

[1]: https://community.box.com/t5/Migrating-and-Previewing-Content/File-Types-and-Fonts-Supported-in-Box-Content-Preview/ta-p/327

This operation is performed by calling function `get_file_thumbnail_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-thumbnail-id/).

<!-- sample get_files_id_thumbnail_id -->

```python
client.files.get_file_thumbnail_by_id(
    thumbnail_file.id, GetFileThumbnailByIdExtension.PNG
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- extension `GetFileThumbnailByIdExtension`
  - The file format for the thumbnail. Example: "png"
- min_height `Optional[int]`
  - The minimum height of the thumbnail.
- min_width `Optional[int]`
  - The minimum width of the thumbnail.
- max_height `Optional[int]`
  - The maximum height of the thumbnail.
- max_width `Optional[int]`
  - The maximum width of the thumbnail.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Optional[ByteStream]`.

When a thumbnail can be created the thumbnail data will be
returned in the body of the response.Sometimes generating a thumbnail can take a few seconds. In these
situations the API returns a `Location`-header pointing to a
placeholder graphic for this file type.

The placeholder graphic can be used in a user interface until the
thumbnail generation has completed. The `Retry-After`-header indicates
when to the thumbnail will be ready. At that time, retry this endpoint
to retrieve the thumbnail.
