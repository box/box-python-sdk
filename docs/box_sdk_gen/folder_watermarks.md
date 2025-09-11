# FolderWatermarksManager

- [Get watermark for folder](#get-watermark-for-folder)
- [Apply watermark to folder](#apply-watermark-to-folder)
- [Remove watermark from folder](#remove-watermark-from-folder)

## Get watermark for folder

Retrieve the watermark for a folder.

This operation is performed by calling function `get_folder_watermark`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folders-id-watermark/).

<!-- sample get_folders_id_watermark -->

```python
client.folder_watermarks.get_folder_watermark(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Watermark`.

Returns an object containing information about the
watermark associated for to this folder.

## Apply watermark to folder

Applies or update a watermark on a folder.

This operation is performed by calling function `update_folder_watermark`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-folders-id-watermark/).

<!-- sample put_folders_id_watermark -->

```python
client.folder_watermarks.update_folder_watermark(folder.id, UpdateFolderWatermarkWatermark(imprint=UpdateFolderWatermarkWatermarkImprintField.DEFAULT))
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- watermark `UpdateFolderWatermarkWatermark`
  - The watermark to imprint on the folder.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Watermark`.

Returns an updated watermark if a watermark already
existed on this folder.Returns a new watermark if no watermark existed on
this folder yet.

## Remove watermark from folder

Removes the watermark from a folder.

This operation is performed by calling function `delete_folder_watermark`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-folders-id-watermark/).

<!-- sample delete_folders_id_watermark -->

```python
client.folder_watermarks.delete_folder_watermark(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

An empty response will be returned when the watermark
was successfully deleted.
