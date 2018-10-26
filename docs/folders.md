Folders
=======

Folder objects represent a folder from a user's account. They can be used to
iterate through a folder's contents, collaborate a folder with another user or
group, and perform other common folder operations (move, copy, delete, etc.).

Get Information About a Folder
------------------------------

To retrieve information about a folder, first call [`client.folder(folder_id)`][folder] to initialize the
[`Folder`][folder_class] object.  Then, call [`folder.get(fields=None, etag=None)`][get] to retrieve data about the
folder.  This method returns a new [`Folder][folder_class] object with fields populated by data from the API, leaving
the original object unmodified.

You can pass a list of `fields` to retrieve from the API in order to filter to just the necessary fields or add
ones not returned by default.

```python
folder = client.folder(folder_id='22222').get()
print('Folder "{0}" has {1} items in it'.format(folder.name, folder.item_collection.total_count))
```

[folder]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.folder
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get
[folder_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder

Get the User's Root Folder
--------------------------

To get the current user's root folder, call [`client.root_folder()`][root_folder] to initialize the appropriate
[`Folder`][folder_class] object.

```python
root_folder = client.root_folder().get()
```

[root_folder]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.root_folder

Get the Items in a Folder
-------------------------

To retrieve the items in a folder, call
[`folder.get_items(limit=None, offset=0, marker=None, use_marker=False, sort=None, direction=None, fields=None)][get_items].
This method returns a `BoxObjectCollection` that allows you to iterate over all the [`Item`][item_class] objects in
the collection.

```python
items = client.folder(folder_id='22222').get_items()
for item in items:
    print('{0} {1} is named "{2}"'.format(item.type.capitalize(), item.id, item.name))
```

[get_items]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.get_items
[item_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item

Update a Folder
---------------

To update a folder's information, call [`folder.update_info(data, etag=None)`][update_info] with a `dict` of properties
to update on the folder.  This method returns a new updated [`Folder`][folder_class] object, leaving the original
object unmodified.

```python
updated_folder = client.folder(folder_id='22222').update_info({
    'name': '[ARCHIVED] Planning documents',
    'description': 'Old planning documents',
})
print('Folder updated!')
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.update_info

Create a Folder
---------------

A folder can be created by calling [`folder.create_subfolder(name)`][create_subfolder] on the parent folder with the
name of the subfolder to be created.  This method returns a new [`Folder`][folder_class] representing the created
subfolder.

```python
subfolder = client.folder('0').create_subfolder('My Stuff')
print('Created subfolder with ID {0}'.format(subfolder.id))
```

[create_subfolder]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.create_subfolder
