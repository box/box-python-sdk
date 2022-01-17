Watermarking
============

The ability to watermark files and folders is represented as a sub-resource on the Files and Folders resources, 
respectively. You can think of the sub-resource as a "label" marking whether the file or folder is watermarked or not. 
If you apply a watermark label to a folder, then all files inside of it will be protected by the watermark (e.g. 
previews will be watermarked). However, those files' watermark sub-resource is independent from the folder that got 
watermarked. This allows you to watermark files and folders independently.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Watermarking](#watermarking)
  - [Get Watermark on File or Folder](#get-watermark-on-file-or-folder)
  - [Apply Watermark on File or Folder](#apply-watermark-on-file-or-folder)
  - [Remove Watermark on File or Folder](#remove-watermark-on-file-or-folder)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Watermark on File or Folder
-------------------------------

To get a watermark object, call  [`file.get_watermark()`][get_file_watermark] or 
[`folder.get_watermark()`][get_folder_watermark] will return the [`Watermark`][watermark_class] object populated with 
data from the API.

<!-- sample get_files_id_watermark -->
```python
watermark = client.file(file_id='12345').get_watermark()
print(f'Watermark created at {watermark.created_at} and modified at {watermark.modified_at}')
```

<!-- sample get_folders_id_watermark -->
```python
watermark = client.folder(folder_id='11111').get_watermark()
print(f'Watermark created at {watermark.created_at} and modified at {watermark.modified_at}')
```

[get_file_watermark]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_watermark()
[get_folder_watermark]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.get_watermark()
[watermark_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.watermark.Watermark

Apply Watermark on File or Folder
---------------------------------

To assign a watermark on a file or folder, call [file.apply_watermark()][apply-file-watermark] or 
[folder.apply_watermark()][apply-folder-watermark] will return the [`Watermark`][watermark_class] object populated with 
data from the API.

<!-- sample put_files_id_watermark -->
```python
watermark = client.file(file_id='12345').apply_watermark()
print(f'Watermark created at {watermark.created_at} and modified at {watermark.modified_at}')
```

<!-- sample put_folders_id_watermark -->
```python
watermark = client.folder(folder_id='11111').apply_watermark()
print(f'Watermark created at {watermark.created_at} and modified at {watermark.modified_at}')
```

[apply-file-watermark]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.file.File.apply_watermark()
[apply_folder_watermark]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.folder.Folder.apply_watermark()
[watermark_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.watermark.Watermark

Remove Watermark on File or Folder
----------------------------------

To remove a watermark from a file or folder, call [file.delete_watermark()][delete-file-watermark] or 
[folder.delete_watermark()][delete-folder-watermark] will return `True` to indicate that the deletion was successful.

<!-- sample delete_files_id_watermark -->
```python
client.file(file_id='12345').delete_watermark()
print('The file watermark was deleted!')
```

<!-- sample delete_folders_id_watermark -->
```python
client.folder(folder_id='11111').delete_watermark()
print('The folder watermark was deleted!')
```

[delete-file-watermark]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.file.File.delete_watermark()
[delete_folder_watermark]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.folder.Folder.delete_watermark()
