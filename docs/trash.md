Trash
=====

Under normal circumstances, when an item in Box is deleted, it is not actually erased immediately. Instead, it is
moved to the Trash. The Trash allows you to recover files and folders that have been deleted. By default, items in
the Trash will be purged after 30 days.


List Trashed Items
-----------------

To retrieve a list of all trashed items, you can use `client.get_trashed_items(offset=None, limit=None, fields=None)`

```python
trashed_items = client.get_trashed_items()
for trashed_item in trashed_items:
    # Do something
```

Get Trashed File or Folder
--------------------------

To retrieve a file from the trash, use `file.get_from_trash(fields=None)`. To retrieve a folder from the trash, use `folder.get_from_trash(fields=None)`.

```python
file_id = '1234'
file_from_trash = client.file(file_id).get_from_trash()
```

```python
folder_id = '5678'
folder_from_trash = client.folder(folder_id).get_from_trash()
```

Restore File or Folder from Trash
---------------------------------

To retore a trashed file, effectively undeleting it, call `file.restore_from_trash(name=None, parent_id=None, fields=None)` or  to restore a trashed folder, call
`folder.restore_from_trash(name=None, parent_id=None, fields=None)`

```python
file_id = '1234'
restored_file = client.file(file_id).restore_from_trash()
```

```python
folder_id = '5678'
restored_folder = client.folder(folder_id).restore_from_trash()
```

In order to avoid conflicts, you can set a new name and new parent folder for the file you wish to restore.

```python
file_id = '1234'
new_name = 'New File Name'
new_parent_id = '1111'
restored_file = client.file(file_id).restore_from_trash(new_name, new_parent_id)
```

```python
folder_id = '1234'
new_name = 'New Folder Name'
new_parent_id = '1111'
restored_folder = client.folder(folder_id).restore_from_trash(new_name, new_parent_id)
```

Permanently Delete File or Folder
---------------------------------

To delete a file from trash, use `file.permanently_delete()` or to delete a folder from trash, use `folder.permanently_delete()`

```python
file_id = '1234'
client.file(file_id).permanently_delete()
```

```python
folder_id = '5678'
client.folder(folder_id).permanently_delete()
```
