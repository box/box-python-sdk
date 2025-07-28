# FileRequestsManager

- [Get file request](#get-file-request)
- [Update file request](#update-file-request)
- [Delete file request](#delete-file-request)
- [Copy file request](#copy-file-request)

## Get file request

Retrieves the information about a file request.

This operation is performed by calling function `get_file_request_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-file-requests-id/).

<!-- sample get_file_requests_id -->

```python
client.file_requests.get_file_request_by_id(file_request_id)
```

### Arguments

- file_request_id `str`
  - The unique identifier that represent a file request. The ID for any file request can be determined by visiting a file request builder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/filerequest/123` the `file_request_id` is `123`. Example: "123"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileRequest`.

Returns a file request object.

## Update file request

Updates a file request. This can be used to activate or
deactivate a file request.

This operation is performed by calling function `update_file_request_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-file-requests-id/).

<!-- sample put_file_requests_id -->

```python
client.file_requests.update_file_request_by_id(
    copied_file_request.id, title="updated title", description="updated description"
)
```

### Arguments

- file_request_id `str`
  - The unique identifier that represent a file request. The ID for any file request can be determined by visiting a file request builder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/filerequest/123` the `file_request_id` is `123`. Example: "123"
- title `Optional[str]`
  - An optional new title for the file request. This can be used to change the title of the file request. This will default to the value on the existing file request.
- description `Optional[str]`
  - An optional new description for the file request. This can be used to change the description of the file request. This will default to the value on the existing file request.
- status `Optional[UpdateFileRequestByIdStatus]`
  - An optional new status of the file request. When the status is set to `inactive`, the file request will no longer accept new submissions, and any visitor to the file request URL will receive a `HTTP 404` status code. This will default to the value on the existing file request.
- is_email_required `Optional[bool]`
  - Whether a file request submitter is required to provide their email address. When this setting is set to true, the Box UI will show an email field on the file request form. This will default to the value on the existing file request.
- is_description_required `Optional[bool]`
  - Whether a file request submitter is required to provide a description of the files they are submitting. When this setting is set to true, the Box UI will show a description field on the file request form. This will default to the value on the existing file request.
- expires_at `Optional[DateTime]`
  - The date after which a file request will no longer accept new submissions. After this date, the `status` will automatically be set to `inactive`. This will default to the value on the existing file request.
- if_match `Optional[str]`
  - Ensures this item hasn't recently changed before making changes. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `412 Precondition Failed` if it has changed since.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileRequest`.

Returns the updated file request object.

## Delete file request

Deletes a file request permanently.

This operation is performed by calling function `delete_file_request_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-file-requests-id/).

<!-- sample delete_file_requests_id -->

```python
client.file_requests.delete_file_request_by_id(updated_file_request.id)
```

### Arguments

- file_request_id `str`
  - The unique identifier that represent a file request. The ID for any file request can be determined by visiting a file request builder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/filerequest/123` the `file_request_id` is `123`. Example: "123"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the file request has been successfully
deleted.

## Copy file request

Copies an existing file request that is already present on one folder,
and applies it to another folder.

This operation is performed by calling function `create_file_request_copy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-file-requests-id-copy/).

<!-- sample post_file_requests_id_copy -->

```python
client.file_requests.create_file_request_copy(
    file_request_id,
    CreateFileRequestCopyFolder(
        id=file_request.folder.id, type=CreateFileRequestCopyFolderTypeField.FOLDER
    ),
)
```

### Arguments

- file_request_id `str`
  - The unique identifier that represent a file request. The ID for any file request can be determined by visiting a file request builder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/filerequest/123` the `file_request_id` is `123`. Example: "123"
- folder `CreateFileRequestCopyFolder`
  - The folder to associate the new file request to.
- title `Optional[str]`
  - An optional new title for the file request. This can be used to change the title of the file request. This will default to the value on the existing file request.
- description `Optional[str]`
  - An optional new description for the file request. This can be used to change the description of the file request. This will default to the value on the existing file request.
- status `Optional[CreateFileRequestCopyStatus]`
  - An optional new status of the file request. When the status is set to `inactive`, the file request will no longer accept new submissions, and any visitor to the file request URL will receive a `HTTP 404` status code. This will default to the value on the existing file request.
- is_email_required `Optional[bool]`
  - Whether a file request submitter is required to provide their email address. When this setting is set to true, the Box UI will show an email field on the file request form. This will default to the value on the existing file request.
- is_description_required `Optional[bool]`
  - Whether a file request submitter is required to provide a description of the files they are submitting. When this setting is set to true, the Box UI will show a description field on the file request form. This will default to the value on the existing file request.
- expires_at `Optional[DateTime]`
  - The date after which a file request will no longer accept new submissions. After this date, the `status` will automatically be set to `inactive`. This will default to the value on the existing file request.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `FileRequest`.

Returns updated file request object.
