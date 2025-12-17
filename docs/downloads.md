# DownloadsManager

- [Download file URL](#download-file-url)
- [Download file](#download-file)
- [Download file](#download-file)

## Download file URL

Get the download URL without downloading the content.

This operation is performed by calling function `get_download_file_url`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-content/).

<!-- sample get_files_id_content -->

```python
client.downloads.get_download_file_url(uploaded_file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- version `Optional[str]`
  - The file version to download.
- access_token `Optional[str]`
  - An optional access token that can be used to pre-authenticate this request, which means that a download link can be shared with a browser or a third party service without them needing to know how to handle the authentication. When using this parameter, please make sure that the access token is sufficiently scoped down to only allow read access to that file and no other files or folders.
- range `Optional[str]`
  - The byte range of the content to download. The format `bytes={start_byte}-{end_byte}` can be used to specify what section of the file to download.
- boxapi `Optional[str]`
  - The URL, and optional password, for the shared link of this item. This header can be used to access items that have not been explicitly shared with a user. Use the format `shared_link=[link]` or if a password is required then use `shared_link=[link]&shared_link_password=[password]`. This header can be used on the file or folder shared, as well as on any files or folders nested within the item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `str`.

Returns the requested file if the client has the **follow
redirects** setting enabled to automatically
follow HTTP `3xx` responses as redirects. If not, the request
will return `302` instead.
For details, see
the [download file guide](https://developer.box.com/guides/downloads/file#download-url).If the file is not ready to be downloaded yet `Retry-After` header will
be returned indicating the time in seconds after which the file will
be available for the client to download.

This response can occur when the file was uploaded immediately before the
download request.

## Download file

Returns the contents of a file in binary format.

This operation is performed by calling function `download_file`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-content/).

<!-- sample get_files_id_content -->

```python
client.downloads.download_file(uploaded_file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- version `Optional[str]`
  - The file version to download.
- access_token `Optional[str]`
  - An optional access token that can be used to pre-authenticate this request, which means that a download link can be shared with a browser or a third party service without them needing to know how to handle the authentication. When using this parameter, please make sure that the access token is sufficiently scoped down to only allow read access to that file and no other files or folders.
- range `Optional[str]`
  - The byte range of the content to download. The format `bytes={start_byte}-{end_byte}` can be used to specify what section of the file to download.
- boxapi `Optional[str]`
  - The URL, and optional password, for the shared link of this item. This header can be used to access items that have not been explicitly shared with a user. Use the format `shared_link=[link]` or if a password is required then use `shared_link=[link]&shared_link_password=[password]`. This header can be used on the file or folder shared, as well as on any files or folders nested within the item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Optional[ByteStream]`.

Returns the requested file if the client has the **follow
redirects** setting enabled to automatically
follow HTTP `3xx` responses as redirects. If not, the request
will return `302` instead.
For details, see
the [download file guide](https://developer.box.com/guides/downloads/file#download-url).If the file is not ready to be downloaded yet `Retry-After` header will
be returned indicating the time in seconds after which the file will
be available for the client to download.

This response can occur when the file was uploaded immediately before the
download request.

## Download file

Download file to a given output stream

This operation is performed by calling function `download_file_to_output_stream`.

```python
client.downloads.download_file_to_output_stream(uploaded_file.id, file_output_stream)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- output_stream `OutputStream`
  - Download file to a given output stream
- version `Optional[str]`
  - The file version to download.
- access_token `Optional[str]`
  - An optional access token that can be used to pre-authenticate this request, which means that a download link can be shared with a browser or a third party service without them needing to know how to handle the authentication. When using this parameter, please make sure that the access token is sufficiently scoped down to only allow read access to that file and no other files or folders.
- range `Optional[str]`
  - The byte range of the content to download. The format `bytes={start_byte}-{end_byte}` can be used to specify what section of the file to download.
- boxapi `Optional[str]`
  - The URL, and optional password, for the shared link of this item. This header can be used to access items that have not been explicitly shared with a user. Use the format `shared_link=[link]` or if a password is required then use `shared_link=[link]&shared_link_password=[password]`. This header can be used on the file or folder shared, as well as on any files or folders nested within the item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.
