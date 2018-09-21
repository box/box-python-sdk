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

Calling `file.get_watermark()` will return the watermark object containing information about the watermark on the file. Or `folder.get_watermark()` will return the watermark object containing information about the watermark on the folder.

```python
watermark_info = client.file('1234').get_watermark()
```

```python
watermark_info = client.folder('5678').get_watermark()
```

Apply Watermark on File or Folder
---------------------------------

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
