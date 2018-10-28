Watermarking
============

The ability to watermark files and folders is represented as a sub-resource on the Files and Folders resources, respectively. You can think of the sub-resource as a "label" marking whether the file or folder is watermarked or not. If you apply a watermark label to a folder, then all files inside of it will be protected by the watermark (e.g. previews will be watermarked). However, those files' watermark sub-resource is independent from the folder that got watermarked. This allows you to watermark files and folders independently.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Watermarking](#watermarking)
  - [Get Watermark on File or Folder](#get-watermark-on-file-or-folder)
  - [Apply Watermark on File or Folder](#apply-watermark-on-file-or-folder)
  - [Remove Watermark on File or Folder](#remove-watermark-on-file-or-folder)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Watermark on File or Folder
-------------------------------

To get a watermark object, first call [`client.file(file_id)`][file]] or [`client.folder(folder_id)`][folder]] to construct the appropriate ['Folder'][folder_class] object, and then calling [`file.get_watermark()`][get] or  [`folder.get_watermark()`][get] will return the [`Watermark`][watermark_class] object populated with data from the API, leaving the original object unmodified.

```python
watermark = client.file('12345').get_watermark()
print('Watermark created at {0} and modified at {1}'.format(watermark.created_at, watermark.modified_at))
```

```python
watermark = client.folder('11111').get_watermark()
print('Watermark created at {0} and modified at {1}'.format(watermark.created_at, watermark.modified_at))
```

[file]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.file
[file_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File
[folder]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.folder
[folder_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get
[watermark_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.watermark.Watermark

Apply Watermark on File or Folder
---------------------------------

To assign a watermark on a file or folder, first call 
To assign a watermark on a file, use `file.apply_watermark()`. To assign a watermark on a folder, use `folder.apply_watermark()`.

```python
watermark_info = client.file('1234').apply_watermark()
```

```python
watermark_info = client.folder('5678').apply_watermark()
```

Remove Watermark on File or Folder
----------------------------------

To remove watermark on a file, use `file.delete_watermark()`. To remove a watermark on a folder, use `folder.delete_watermark()`

```python
client.file('1234').delete_watermark()
```

```python
client.folder('5678').delete_watermark()
```
