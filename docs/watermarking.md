Watermarking
======

The ability to watermark files and folders is represented as a sub-resource on the Files and Folders resources, respectively. You can think of the sub-resource as a "label" marking whether the file or folder is watermarked or not. If you apply a watermark label to a folder, then all files inside of it will be protected by the watermark (e.g. previews will be watermarked). However, those files' watermark sub-resource is independent from the folder that got watermarked. This allows you to watermark files and folders independently.

Get Watermark on File
---------------------

Calling `file.get_watermark()` will return the watermark object containing information about the watermark on the file.

```python
watermark_info = client.file('1234').get_watermark()
```

Apply Watermark on File
-----------------------

To assign a watermark on a file, use `file.apply_watermark()`.

```python
watermark_info = client.file('1234').apply_watermark()
```

Remove Watermark on File
------------------------

To remove watermark on a file, use `file.delete_watermark()`.

```python
client.file('1234').delete_watermark()
```

Get Watermark on Folder
-----------------------

Calling `folder.get_watermark()` will return the watermark object containing information about the watermark on the folder.

```python
watermark_info = client.folder('5678').get_watermark()
```

Apply Watermark on Folder
-------------------------

To assign a watermark on a folder, use `folder.apply_watermark()`.

```python
watermark_info = client.folder('5678').apply_watermark()
```

Remove Watermark on Folder
--------------------------

To remove watermark on a folder, use `folder.delete_watermark()`.

```python
client.folder('5678').delete_watermark()
```