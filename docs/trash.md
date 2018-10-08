Trash
=====

Under normal circumstances, when an item in Box is deleted, it is not actually erased immediately. Instead, it is
moved to the Trash. The Trash allows you to recover files and folders that have been deleted. By default, items in
the Trash will be purged after 30 days.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [List Trashed Items](#list-trashed-items)
- [Get Trashed Items](#get-trashed-items)
- [Restore Item from Trash](#restore-item-from-trash)
- [Permanently Delete Item](#permanently-delete-item)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Trashed Items
------------------

To retrieve a list of all trashed items, you can use `client.trash().get__items(limit=None, offset=None, fields=None)`

```python
trashed_items = client.trash().get_items()
for trashed_item in trashed_items:
    # Do something
```

Get Trashed Items
-----------------

To retrieve a file, folder, weblink from the trash, use `client.trash.get_item_info(item, fields=None)`. 

```python
file_info_to_retrieve = client.file('11111')
file_from_trash = client.trash().get_item_info(file_info_to_retrieve)
```

```python
folder = client.folder('22222')
folder_from_trash = client.trash().get_item_info(folder)
```

```python
web_link = client.web_link('33333')
web_link_from_trash = client.trash().get_item_info(web_link)
```

Restore Item from Trash
-----------------------

To retore a trashed item, effectively undeleting it, call `client.trash().restore_item(item, name=None, parent_folder=None, fields=None)`.

```python
file_to_restore = client.file('11111')
restored_file = client.trash().restore_item(file_to_restore)
```

```python
folder_to_restore = client.folder('22222')
restored_folder = client.trash().restore_item(folder_to_restore)
```

```python
web_link_to_restore = client.web_link('33333')
restored_web_link = client.trash().restore_item(web_link_to_restore)
```

In order to avoid conflicts, you can set a new name and new parent folder for the item you wish to restore.

```python
file_to_restore = client.file('11111')
new_name = 'New File Name'
new_parent_folder = client.folder('22222')
restored_file = client.trash().restore_item(file_to_restore, new_name, new_parent_folder)
```

Permanently Delete Item
-----------------------

To delete an item from trash, use `client.trash().permanently_delete_item(item)`.

```python
file_to_delete = client.file('11111')
client.trash().permanently_delete_item(file_to_delete)
```

```python
folder = client.folder('22222')
client.trash().permanently_delete_item(folder)
```

```python
web_link = client.web_link('33333')
client.trash().permanently_delete_item(web_link)
```
