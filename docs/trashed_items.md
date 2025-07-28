# TrashedItemsManager

- [List trashed items](#list-trashed-items)

## List trashed items

Retrieves the files and folders that have been moved
to the trash.

Any attribute in the full files or folders objects can be passed
in with the `fields` parameter to retrieve those specific
attributes that are not returned by default.

This endpoint defaults to use offset-based pagination, yet also supports
marker-based pagination using the `marker` parameter.

This operation is performed by calling function `get_trashed_items`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folders-trash-items/).

<!-- sample get_folders_trash_items -->

```python
client.trashed_items.get_trashed_items()
```

### Arguments

- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- usemarker `Optional[bool]`
  - Specifies whether to use marker-based pagination instead of offset-based pagination. Only one pagination method can be used at a time. By setting this value to true, the API will return a `marker` field that can be passed as a parameter to this endpoint to get the next page of the response.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- direction `Optional[GetTrashedItemsDirection]`
  - The direction to sort results in. This can be either in alphabetical ascending (`ASC`) or descending (`DESC`) order.
- sort `Optional[GetTrashedItemsSort]`
  - Defines the **second** attribute by which items are sorted. Items are always sorted by their `type` first, with folders listed before files, and files listed before web links. This parameter is not supported when using marker-based pagination.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Items`.

Returns a list of items that have been deleted.
