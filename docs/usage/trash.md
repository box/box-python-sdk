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

To retrieve all trashed items for an enterprise, call [`client.trash().get_items(imit=None, offset=None, fields=None)`][get_trashed_items]. 
This method returns a `BoxObjectCollection` that allows you to iterate over the [`Trash`][trash] objects in the 
collection.

```python
trashed_items = client.trash().get_items()
for trashed_item in trashed_items:
    print('The item ID is {0} and the item name is {1}'.format(trashed_item.id, trashed_item.name))
```

[get_trashed_item]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.trash.Trash.get_trashed_items
[trash]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.trash.Trash

Get Trashed Items
-----------------

To get a trashed item, call [`client.trash().get_item(item, fields)`][get_item] with the item you wish to retrieve passed in. 
This method will return the ['Item'][item] object populated with data from the API.

```python
file_to_retrieve = client.file(file_id='11111')
file_from_trash = client.trash().get_item(file_to_retrieve)
print('File ID is {0} and name is {1}'.format(file_from_trash.id, file_from_trash.name))
```

```python
folder = client.folder(folder_id='22222')
folder_from_trash = client.trash().get_item(folder)
print('Folder ID is {0} and name is {1}'.format(folder_from_trash.id, folder_from_trash.name))
```

```python
web_link = client.web_link(web_link_i='33333')
web_link_from_trash = client.trash().get_item(web_link)
print('Web link ID is {0} and name is {1}'.format(web_link_from_trash.id, web_link_from_trash.name))
```

[item]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item
[get_item]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.trash.Trash.get_item

Restore Item from Trash
-----------------------

To retore a trashed item, effectively undeleting it, call [`client.trash().restore(item, name=None, parent_folder, fields=None)`][restore_item] 
with the constructed [`Item`][item_class] object will let you restore the specific object from your trash. This method 
will return a [`Item`][item_class] object populated with data from the API, leaving the original object unmodified.

```python
file_to_restore = client.file(file_id='11111')
restored_file = client.trash().restore_item(file_to_restore)
print('File ID is {0} and name is {1}'.format(restored_file.id, restored_file.name))
```

```python
folder_to_restore = client.folder(folder_id='22222')
restored_folder = client.trash().restore_item(folder_to_restore)
print('Folder ID is {0} and name is {1}'.format(restored_folder.id, restored_folder.name))
```

```python
web_link_to_restore = client.web_link(web_link_id='33333')
restored_web_link = client.trash().restore_item(web_link_to_restore)
print('Web link ID is {0} and name is {1}'.format(restored_web_link.id, restored_web_link.name))
```

In order to avoid conflicts, you can set a new name and new parent folder for the item you wish to restore.

```python
file_to_restore = client.file(file_id='11111')
new_name = 'New File Name'
new_parent_folder = client.folder(folder_id='22222')
restored_file = client.trash().restore_item(file_to_restore, new_name, new_parent_folder)
print('New name for file is {0} and new parent folder is {1}'.format(restored_file.name, restored_file.parent.name))
```

[item_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item
[restore_item]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.trash.Trash.restore_item

Permanently Delete Item
-----------------------

To delete an [`Item`][item_class] object from trash, call [`client.trash().permanently_delete_item(item)`][delete]. 
This method returns `True` to indicate that the deletion was successful.

```python
file_to_delete = client.file(file_id='11111')
client.trash().permanently_delete_item(file_to_delete)
print('The file was deleted from trash!')
```

```python
folder = client.folder(folder_id='22222')
client.trash().permanently_delete_item(folder)
print('The folder was deleted from trash!')
```

```python
web_link = client.web_link(web_link_id='33333')
client.trash().permanently_delete_item(web_link)
print('The web link was deleted from trash!')
```

[item_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item
[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.trash.Trash.permanently_delete
