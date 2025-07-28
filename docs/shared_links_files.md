# SharedLinksFilesManager

- [Find file for shared link](#find-file-for-shared-link)
- [Get shared link for file](#get-shared-link-for-file)
- [Add shared link to file](#add-shared-link-to-file)
- [Update shared link on file](#update-shared-link-on-file)
- [Remove shared link from file](#remove-shared-link-from-file)

## Find file for shared link

Returns the file represented by a shared link.

A shared file can be represented by a shared link,
which can originate within the current enterprise or within another.

This endpoint allows an application to retrieve information about a
shared file when only given a shared link.

The `shared_link_permission_options` array field can be returned
by requesting it in the `fields` query parameter.

This operation is performed by calling function `find_file_for_shared_link`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shared-items/).

<!-- sample get_shared_items -->

```python
user_client.shared_links_files.find_file_for_shared_link(
    "".join(
        [
            "shared_link=",
            file_from_api.shared_link.url,
            "&shared_link_password=Secret123@",
        ]
    )
)
```

### Arguments

- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- if_none_match `Optional[str]`
  - Ensures an item is only returned if it has changed. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `304 Not Modified` if the item has not changed since.
- boxapi `str`
  - A header containing the shared link and optional password for the shared link. The format for this header is as follows: `shared_link=[link]&shared_link_password=[password]`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns a full file resource if the shared link is valid and
the user has access to it.

## Get shared link for file

Gets the information for a shared link on a file.

This operation is performed by calling function `get_shared_link_for_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id--get-shared-link/).

<!-- sample get_files_id#get_shared_link -->

```python
client.shared_links_files.get_shared_link_for_file(file_id, "shared_link")
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns the base representation of a file with the
additional shared link information.

## Add shared link to file

Adds a shared link to a file.

This operation is performed by calling function `add_share_link_to_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-files-id--add-shared-link/).

<!-- sample put_files_id#add_shared_link -->

```python
client.shared_links_files.add_share_link_to_file(
    file_id,
    "shared_link",
    shared_link=AddShareLinkToFileSharedLink(
        access=AddShareLinkToFileSharedLinkAccessField.OPEN, password="Secret123@"
    ),
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- shared_link `Optional[AddShareLinkToFileSharedLink]`
  - The settings for the shared link to create on the file. Use an empty object (`{}`) to use the default settings for shared links.
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns the base representation of a file with a new shared
link attached.

## Update shared link on file

Updates a shared link on a file.

This operation is performed by calling function `update_shared_link_on_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-files-id--update-shared-link/).

<!-- sample put_files_id#update_shared_link -->

```python
client.shared_links_files.update_shared_link_on_file(
    file_id,
    "shared_link",
    shared_link=UpdateSharedLinkOnFileSharedLink(
        access=UpdateSharedLinkOnFileSharedLinkAccessField.COLLABORATORS
    ),
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- shared_link `Optional[UpdateSharedLinkOnFileSharedLink]`
  - The settings for the shared link to update.
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns a basic representation of the file, with the updated shared
link attached.

## Remove shared link from file

Removes a shared link from a file.

This operation is performed by calling function `remove_shared_link_from_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-files-id--remove-shared-link/).

<!-- sample put_files_id#remove_shared_link -->

```python
client.shared_links_files.remove_shared_link_from_file(
    file_id, "shared_link", shared_link=create_null()
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- shared_link `Optional[RemoveSharedLinkFromFileSharedLink]`
  - By setting this value to `null`, the shared link is removed from the file.
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileFull`.

Returns a basic representation of a file, with the shared link removed.
