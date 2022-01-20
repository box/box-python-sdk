Collections
===========

Collections allow users to mark specific files, folders and web links to make it easier to find them.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Get a User's Collections](#get-a-users-collections)
- [Get the Items in a Collection](#get-the-items-in-a-collection)
- [Add an Item to a Collection](#add-an-item-to-a-collection)
- [Remove an Item from a Collection](#remove-an-item-from-a-collection)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get a User's Collections
------------------------

To get all collections belonging to a user, call [`client.collections(limit=None, offset=0, fields=None)`][collections].
This method returns a `BoxObjectCollection` that you can use to iterate over all the
[`Collection`][collection_class] objects in the set.

<!-- sample get_collections -->
```python
collections = client.collections()
for collection in collections:
    print(f'Collection "{collection.name}" has ID {collection.id}')
```

[collections]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.collections
[collection_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collection.Collection

Get the Items in a Collection
-----------------------------

To retrieve a list of items contained in a collection, call
[`collection.get_items(limit=None, offset=0, fields=None)`][get_items].  This method returns a
`BoxObjectCollection` that you can use to iterate over all the [`BaseItem`][base_item_class] objects in
the collection. [`BaseItem`][base_item_class] is a super class for files, folders and web links.

<!-- sample get_collections_id_items -->
```python
items = client.collection(collection_id='12345').get_items()
for item in items:
    print(f'{item.type.capitalize()} "{item.name}" is in the collection')
```

[get_items]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collection.Collection.get_items
[base_item_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem

Add an Item to a Collection
----------------------

To add an [`BaseItem`][base_item_class] to a collection, call [`item.add_to_collection(collection)`][add_to_collection] with the
[`Collection`][collection_class] you want to add the item to.  This method returns the updated [`BaseItem`][base_item_class]
object.

<!-- sample put_files_id add_to_collection -->
```python
collection = client.collection(collection_id='12345')
updated_file = client.file(file_id='11111').add_to_collection(collection)
print(f'File "{updated_file.name}" added to collection!')
```

[add_to_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.add_to_collection

Remove an Item from a Collection
---------------------------

To remove an [`BaseItem`][base_item_class]  from a collection, call
[`item.remove_from_collection(collection)`][remove_from_collection] with the [`Collection`][collection_class] you want
to remove the item from.  This method returns the updated [`BaseItem`][base_item_class]  object.

<!-- sample put_files_id remove_from_collection -->
```python
collection = client.collection(collection_id='12345')
updated_file = client.file(file_id='11111').remove_from_collection(collection)
print(f'File "{updated_file.name}" removed from collection!')
```

[remove_from_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.remove_from_collection
