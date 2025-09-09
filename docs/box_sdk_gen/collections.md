# CollectionsManager

- [List all collections](#list-all-collections)
- [List collection items](#list-collection-items)
- [Get collection by ID](#get-collection-by-id)

## List all collections

Retrieves all collections for a given user.

Currently, only the `favorites` collection
is supported.

This operation is performed by calling function `get_collections`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collections/).

<!-- sample get_collections -->

```python
client.collections.get_collections()
```

### Arguments

- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Collections`.

Returns all collections for the given user.

## List collection items

Retrieves the files and/or folders contained within
this collection.

This operation is performed by calling function `get_collection_items`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collections-id-items/).

<!-- sample get_collections_id_items -->

```python
client.collections.get_collection_items(favourite_collection.id)
```

### Arguments

- collection_id `str`
  - The ID of the collection. Example: "926489"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ItemsOffsetPaginated`.

Returns an array of items in the collection.

## Get collection by ID

Retrieves a collection by its ID.

This operation is performed by calling function `get_collection_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collections-id/).

<!-- sample get_collections_id -->

```python
client.collections.get_collection_by_id(collections.entries[0].id)
```

### Arguments

- collection_id `str`
  - The ID of the collection. Example: "926489"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Collection`.

Returns an array of items in the collection.
