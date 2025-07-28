# TrashedWebLinksManager

- [Restore web link](#restore-web-link)
- [Get trashed web link](#get-trashed-web-link)
- [Permanently remove web link](#permanently-remove-web-link)

## Restore web link

Restores a web link that has been moved to the trash.

An optional new parent ID can be provided to restore the web link to in case
the original folder has been deleted.

This operation is performed by calling function `restore_weblink_from_trash`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-web-links-id/).

<!-- sample post_web_links_id -->

```python
client.trashed_web_links.restore_weblink_from_trash(weblink.id)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- name `Optional[str]`
  - An optional new name for the web link.
- parent `Optional[RestoreWeblinkFromTrashParent]`
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TrashWebLinkRestored`.

Returns a web link object when it has been restored.

## Get trashed web link

Retrieves a web link that has been moved to the trash.

This operation is performed by calling function `get_trashed_web_link_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-web-links-id-trash/).

<!-- sample get_web_links_id_trash -->

```python
client.trashed_web_links.get_trashed_web_link_by_id(weblink.id)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TrashWebLink`.

Returns the web link that was trashed,
including information about when the it
was moved to the trash.

## Permanently remove web link

Permanently deletes a web link that is in the trash.
This action cannot be undone.

This operation is performed by calling function `delete_trashed_web_link_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-web-links-id-trash/).

<!-- sample delete_web_links_id_trash -->

```python
client.trashed_web_links.delete_trashed_web_link_by_id(weblink.id)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the web link was
permanently deleted.
