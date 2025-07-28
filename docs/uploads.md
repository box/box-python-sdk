# UploadsManager

- [Upload file version](#upload-file-version)
- [Preflight check before upload](#preflight-check-before-upload)
- [Upload file](#upload-file)
- [Upload a file with a preflight check](#upload-a-file-with-a-preflight-check)

## Upload file version

Update a file's content. For file sizes over 50MB we recommend
using the Chunk Upload APIs.

The `attributes` part of the body must come **before** the
`file` part. Requests that do not follow this format when
uploading the file will receive a HTTP `400` error with a
`metadata_after_file_contents` error code.

This operation is performed by calling function `upload_file_version`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-files-id-content/).

<!-- sample post_files_id_content -->

```python
client.uploads.upload_file_version(
    uploaded_file.id,
    UploadFileVersionAttributes(name=new_file_version_name),
    new_file_content_stream,
)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- attributes `UploadFileVersionAttributes`
  - The additional attributes of the file being uploaded. Mainly the name and the parent folder. These attributes are part of the multi part request body and are in JSON format. <Message warning> The `attributes` part of the body must come **before** the `file` part. Requests that do not follow this format when uploading the file will receive a HTTP `400` error with a `metadata_after_file_contents` error code. </Message>
- file `ByteStream`
  - The content of the file to upload to Box. <Message warning> The `attributes` part of the body must come **before** the `file` part. Requests that do not follow this format when uploading the file will receive a HTTP `400` error with a `metadata_after_file_contents` error code. </Message>
- file_file_name `Optional[str]`
- file_content_type `Optional[str]`
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- if_match `Optional[str]`
  - Ensures this item hasn't recently changed before making changes. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `412 Precondition Failed` if it has changed since.
- content_md_5 `Optional[str]`
  - An optional header containing the SHA1 hash of the file to ensure that the file was not corrupted in transit.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Files`.

Returns the new file object in a list.

## Preflight check before upload

Performs a check to verify that a file will be accepted by Box
before you upload the entire file.

This operation is performed by calling function `preflight_file_upload_check`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/options-files-content/).

<!-- sample options_files_content -->

```python
client.uploads.preflight_file_upload_check(
    name=new_file_name, size=1024 * 1024, parent=PreflightFileUploadCheckParent(id="0")
)
```

### Arguments

- name `Optional[str]`
  - The name for the file.
- size `Optional[int]`
  - The size of the file in bytes.
- parent `Optional[PreflightFileUploadCheckParent]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `UploadUrl`.

If the check passed, the response will include a session URL that
can be used to upload the file to.

## Upload file

Uploads a small file to Box. For file sizes over 50MB we recommend
using the Chunk Upload APIs.

The `attributes` part of the body must come **before** the
`file` part. Requests that do not follow this format when
uploading the file will receive a HTTP `400` error with a
`metadata_after_file_contents` error code.

This operation is performed by calling function `upload_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-files-content/).

<!-- sample post_files_content -->

```python
client.uploads.upload_file(
    UploadFileAttributes(
        name=new_file_name, parent=UploadFileAttributesParentField(id="0")
    ),
    file_content_stream,
)
```

### Arguments

- attributes `UploadFileAttributes`
  - The additional attributes of the file being uploaded. Mainly the name and the parent folder. These attributes are part of the multi part request body and are in JSON format. <Message warning> The `attributes` part of the body must come **before** the `file` part. Requests that do not follow this format when uploading the file will receive a HTTP `400` error with a `metadata_after_file_contents` error code. </Message>
- file `ByteStream`
  - The content of the file to upload to Box. <Message warning> The `attributes` part of the body must come **before** the `file` part. Requests that do not follow this format when uploading the file will receive a HTTP `400` error with a `metadata_after_file_contents` error code. </Message>
- file_file_name `Optional[str]`
- file_content_type `Optional[str]`
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- content_md_5 `Optional[str]`
  - An optional header containing the SHA1 hash of the file to ensure that the file was not corrupted in transit.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Files`.

Returns the new file object in a list.

## Upload a file with a preflight check

Upload a file with a preflight check

This operation is performed by calling function `upload_with_preflight_check`.

```python
client.uploads.upload_with_preflight_check(
    UploadWithPreflightCheckAttributes(
        name=new_file_name,
        size=-1,
        parent=UploadWithPreflightCheckAttributesParentField(id="0"),
    ),
    file_content_stream,
)
```

### Arguments

- attributes `UploadWithPreflightCheckAttributes`
- file `ByteStream`
  - The content of the file to upload to Box. <Message warning> The `attributes` part of the body must come **before** the `file` part. Requests that do not follow this format when uploading the file will receive a HTTP `400` error with a `metadata_after_file_contents` error code. </Message>
- file_file_name `Optional[str]`
- file_content_type `Optional[str]`
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- content_md_5 `Optional[str]`
  - An optional header containing the SHA1 hash of the file to ensure that the file was not corrupted in transit.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Files`.
