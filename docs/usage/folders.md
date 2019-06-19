Folders
=======

Folder objects represent a folder from a user's account. They can be used to
iterate through a folder's contents, collaborate a folder with another user or
group, and perform other common folder operations (move, copy, delete, etc.).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get Information About a Folder](#get-information-about-a-folder)
- [Get the User's Root Folder](#get-the-users-root-folder)
- [Get the Items in a Folder](#get-the-items-in-a-folder)
- [Update a Folder](#update-a-folder)
- [Create a Folder](#create-a-folder)
- [Copy a Folder](#copy-a-folder)
- [Move a Folder](#move-a-folder)
- [Delete a Folder](#delete-a-folder)
- [Create a Shared Link](#create-a-shared-link)
- [Set Metadata](#set-metadata)
- [Get Metadata](#get-metadata)
- [Remove Metadata](#remove-metadata)
- [Get All Metadata](#get-all-metadata)
- [Get Metadata For Folder Items](#get-metadata-for-folder-items)
- [Set a Classification](#set-a-classification)
- [Retrieve a Classification](#retrieve-a-classification)
- [Remove a Classification](#remove-a-classification)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Information About a Folder
------------------------------

To retrieve information about a folder, first call [`client.folder(folder_id)`][folder] to initialize the
[`Folder`][folder_class] object.  Then, call [`folder.get(fields=None, etag=None)`][get] to retrieve data about the
folder.  This method returns a new [`Folder][folder_class] object with fields populated by data from the API, leaving
the original object unmodified.

You can pass a list of `fields` to retrieve from the API in order to filter to just the necessary fields or add
ones not returned by default.

<!-- sample get_folders_id -->
```python
folder = client.folder(folder_id='22222').get()
print('Folder "{0}" has {1} items in it'.format(
    folder.name,
    folder.item_collection.total_count,
))
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

<!-- sample get_folders_id_items -->
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

<!-- sample put_folders_id -->
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

<!-- sample post_folders -->
```python
subfolder = client.folder('0').create_subfolder('My Stuff')
print('Created subfolder with ID {0}'.format(subfolder.id))
```

[create_subfolder]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.create_subfolder

Copy a Folder
-------------

A folder can be copied into a new parent folder by calling [`folder.copy(parent_folder, name=None)`][copy] with the
destination folder and an optional new name for the file in case there is a name conflict in the destination folder.
This method returns a new [`Folder`][folder_class] object representing the copy of the folder in the destination folder.

<!-- sample post_folders_id_copy -->
```python
folder_id = '22222'
destination_folder_id = '44444'

folder_to_copy = client.folder(folder_id)
destination_folder = client.folder(destination_folder_id)

folder_copy = folder_to_copy.copy(destination_folder)
print('Folder "{0}" has been copied into folder "{1}"'.format(folder_copy.name, folder_copy.parent.name))
```

[copy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.copy

Move a Folder
-------------

To move a folder from one parent folder into another, call [`folder.move(parent_folder, name=None)`][move] with the
destination folder to move the folder into.  You can optionally provide a `name` parameter to automatically rename the
folder in case of a name conflict in the destination folder.  This method returns the updated [`Folder`][folder_class]
object in the new folder.

```python
folder_id = '11111'
destination_folder_id = '44444'

folder_to_move = client.folder(folder_id)
destination_folder = client.folder(destination_folder_id)

moved_folder = folder_to_move.move(destination_folder)
print('Folder "{0}" has been moved into folder "{1}"'.format(moved_folder.name, moved_folder.parent.name))
```

[move]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.move

Delete a Folder
---------------

Calling the [`folder.delete(recursive=True, etag=None)`][delete] method will delete the folder.  Depending on enterprise
settings, this will either move the folder to the user's trash or permanently delete the folder.  This method returns
`True` to signify that the deletion was successful.

By default, the method will delete the folder and all of its contents; to fail the deletion if the folder is not empty,
set the `recursive` parameter to `False`.

<!-- sample delete_folders_id -->
```python
client.folder(folder_id='22222').delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.delete

Create a Shared Link
--------------------

A shared link for a folder can be generated by calling
[`folder.get_shared_link(access=None, etag=None, unshared_at=None, allow_download=None, allow_preview=None, password=None)`][get_shared_link].
This method returns a `unicode` string containing the shared link URL.

```python
url = client.folder(folder_id='22222').get_shared_link()
print('The folder shared link URL is: {0}'.format(url))
```

[get_shared_link]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_shared_link


Set Metadata
------------

To set metadata on a folder call the [`folder.metadata(scope='global', template='properties')`][metadata]
to specify the scope and template key of the metadata template to attach. Then, call the [`metadata.set(data)`][metadata_set] method with the key/value pairs to attach. This method returns a `dict` containing the applied metadata instance.

Note: This method will unconditionally apply the provided metadata, overwriting the existing metadata for the keys provided.
To specifically create or update metadata, see the `create()` or `update()` methods.

```python
metadata = {
    'foo': 'bar',
}
applied_metadata = client.folder(folder_id='11111').metadata(scope='enterprise', template='testtemplate').set(metadata)
print('Set metadata in instance ID {0}'.format(applied_metadata['$id']))
```

Metadata can be added to a folder either as free-form key/value pairs or from an existing template.  To add metadata to
a folder, first call [`folder.metadata(scope='global', template='properties')`][metadata] to specify the scope
and template key of the metadata template to attach (or use the default values to attach free-form keys and values).
Then, call [`metadata.create(data)`][metadata_create] with the key/value pairs to attach.  This method can only be used
to attach a given metadata template to the folder for the first time, and returns a `dict` containing the applied
metadata instance.

Note: This method will only succeed if the provided metadata template is not currently applied to the folder, otherwise it will 
fail with a Conflict error.

<!-- sample post_folders_id_metadata_id_id -->
```python
metadata = {
    'foo': 'bar',
    'baz': 'quux',
}

applied_metadata = client.folder(folder_id='22222').metadata().create(metadata)
print('Applied metadata in instance ID {0}'.format(applied_metadata['$id']))
```

Updating metadata values is performed via a series of discrete operations, which are applied atomically against the
existing folder metadata.  First, specify which metadata will be updated by calling
[`folder.metadata(scope='global', template='properties')`][metadata].  Then, start an update sequence by calling
[`metadata.start_update()`][metadata_start_update] and add update operations to the returned
[`MetadataUpdate`][metadata_update_obj].  Finally, perform the update by calling
[`metadata.update(metadata_update)`][metadata_update].  This final method returns a `dict` of the updated metadata
instance.

Note: This method will only succeed if the provided metadata template has already been applied to the folder; If the folder does not
have existing metadata, this method will fail with a Not Found error. This is useful you know the file will already have metadata applied,
since it will save an API call compared to `set()`.

<!-- sample put_folders_id_metadata_id_id -->
```python
folder = client.folder(folder_id='22222')
folder_metadata = folder.metadata(scope='enterprise', template='myMetadata')

updates = folder_metadata.start_update()
updates.add('/foo', 'bar')
updates.update('/baz', 'murp', old_value='quux')  # Ensure the old value was "quux" before updating to "murp"

updated_metadata = folder_metadata.update(updates)
print('Updated metadata on folder!')
print('foo is now {0} and baz is now {1}'.format(updated_metadata['foo'], updated_metadata['baz']))
```

[set_metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.set
[metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.metadata
[metadata_create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.create
[metadata_start_update]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.start_update
[metadata_update_obj]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.MetadataUpdate
[metadata_update]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.update

Get Metadata
------------

To retrieve the metadata instance on a folder for a specific metadata template, first call
[`folder.metadata(scope='global', template='properties')`][metadata] to specify the scope and template key of
the metadata template to retrieve, then call [`metadata.get()`][metadata_get] to retrieve the metadata values attached
to the folder.  This method returns a `dict` containing the applied metadata instance.

<!-- sample get_folders_id_metadata_id_id -->
```python
metadata = client.folder(folder_id='22222').metadata(scope='enterprise', template='myMetadata').get()
print('Got metadata instance {0}'.format(metadata['$id']))
```

[metadata_get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.get

Remove Metadata
---------------

To remove a metadata instance from a folder, call
[`folder.metadata(scope='global', template='properties')`][metadata] to specify the scope and template key of the
metadata template to remove, then call [`metadata.delete()`][metadata_delete] to remove the metadata from the folder.
This method returns `True` to indicate that the removal succeeded.

<!-- sample delete_folders_id_metadata_id_id -->
```python
client.folder(folder_id='11111').metadata(scope='enterprise', template='myMetadata').delete()
```

[metadata_delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.delete

Get All Metadata
----------------

To retrieve all metadata attached to a folder, call [`folder.get_all_metadata()`][get_all_metadata].  This method
returns a [`BoxObjectCollection`][box_object_collection] that can be used to iterate over the `dict`s representing each
metadata instance attached to the folder.

<!-- sample get_folders_id_metadata -->
```python
folder_metadata = client.folder(folder_id='22222').get_all_metadata()
for instance in folder_metadata:
    if 'foo' in instance:
        print('Metadata instance {0} has value "{1}" for foo'.format(instance['id'], instance['foo']))
```

[get_all_metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_all_metadata

Get Metadata For Folder Items
-----------------------------

When fetching folder items, you may wish to retrieve metadata for the items simultaneously to avoid needing to make
an API call for each item.  You can retrieve up to 3 metadata instances per item by passing the special
`metadata.<scope>.<templateKey>` field to
[`folder.get_items(limit=None, offset=0, marker=None, use_marker=False, sort=None, direction=None, fields=None)`][get_items].
The metadata is available as a multi-level `dict` on the returned [`Item`][item_class] objects.

```python
fields = [
    'type',
    'id',
    'name',
    'metadata.enterprise.vendorContract',
]
items = client.folder(folder_id='22222').get_items(fields=fields)
for item in items:
    if item.metadata:
        metadata = item.metadata['enterprise']['vendorContract']
        print('{0} {1} is a vendor contract with vendor name {2}'.format(
            item.type.capitalize(),
            item.id,
            metadata['vendorName'],
        ))
```

Set a Classification
--------------------

It is important to note that this feature is available only if you have Governance.

To add classification to a [`Folder`][folder_class], call [`folder.set_classification(classification)`][set_classification].
This method returns the classification type on the [`Folder`][folder_class] object. If a classification already exists then 
this call will update the existing classification with the new [`ClassificationType`][classification_type_class].

```python
from boxsdk.object.item import ClassificationType

classification = client.folder(folder_id='11111').set_classification(ClassificationType.PUBLIC)
print('Classification Type is: {0}'.format(classification))
```

The set method will always work no matter the state your [`Folder`][folder_class] is in. For cases already where a
classification value already exists [`set_classification(classification)`][set_classification] may make multiple 
API calls. 

Alternatively, if you already know you have a classification and you are simple updating it, you can use the 
[`update_classification(classification)`][update_classification]. This will ultimately help you save one extra API call.

```python
classification = client.folder(folder_id='11111').update_classification(ClassificationType.NONE)
print('Classification Type is: {0}'.format(classification))
```

[set_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.set_classification
[update_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.update_classification
[classification_type_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.ClassificationType

Retrieve a Classification
-------------------------

To retrieve a classification from a [`Folder`][folder_class], call [`folder.get_classification()`][get_classification].
This method returns the classification type on the [`Folder`][folder_class] object.

```python
classification = client.folder(folder_id='11111').get_classification()
print('Classification Type is: {0}'.format(classification))
```

[get_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_classification

Remove a Classification
-----------------------

To remove a classification from a [`Folder`][folder_class], call [`folder.remove_classification()`][remove_classification].

```python
client.folder(folder_id='11111').remove_classification()
```

[remove_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.remove_classification
