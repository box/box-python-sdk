Collections
===========

Collections allow users to mark specific files and folders to make it easier to find them.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get a User's Collections](#get-a-users-collections)
- [Get the Items in a Collection](#get-the-items-in-a-collection)
- [Add Item to Collection](#add-item-to-collection)
- [Remove Item from Collection](#remove-item-from-collection)

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
    print('Collection "{0}" has ID {1}'.format(collection.name, collection.id))
```

[collections]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.collections
[collection_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collection.Collection

Get the Items in a Collection
-----------------------------

To retrieve a list of items contained in a collection, call
[`collection.get_items(limit=None, offset=0, fields=None)`][get_items].  This method returns a
`BoxObjectCollection` that you can use to iterate over all the [`Item`][item_class] objects in
the collection.

<!-- sample get_collections_id_items -->
```python
items = client.collection(collection_id='12345').get_items()
for item in items:
    print('{0} "{1}" is in the collection'.format(item.type.capitalize(), item.name))
```

[get_items]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collection.Collection.get_items
[item_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item

Add Item to Collection
----------------------

To add an [`Item`][item_class] to a collection, call [`item.add_to_collection(collection)`][add_to_collection] with the
[`Collection`][collection_class] you want to add the item to.  This method returns the updated [`Item`][item_class]
object.

```python
collection = client.collection(collection_id='12345')
updated_file = client.file(file_id='11111').add_to_collection(collection)
print('File "{0}" added to collection!'.format(updated_file.name))
```

[add_to_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.add_to_collection

Remove Item from Collection
---------------------------

To remove an [`Item`][item_class] from a collection, call
[`item.remove_from_collection(collection)`][remove_from_collection] with the [`Collection`][collection_class] you want
to remove the item from.  This method returns the updated [`Item`][item_class] object.

```python
collection = client.collection(collection_id='12345')
updated_file = client.file(file_id='11111').remove_from_collection(collection)
print('File "{0}" removed from collection!'.format(updated_file.name))
```

[remove_from_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.remove_from_collection
