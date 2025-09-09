# WebLinksManager

- [Create web link](#create-web-link)
- [Get web link](#get-web-link)
- [Update web link](#update-web-link)
- [Remove web link](#remove-web-link)

## Create web link

Creates a web link object within a folder.

This operation is performed by calling function `create_web_link`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-web-links/).

<!-- sample post_web_links -->

```python
client.web_links.create_web_link('https://www.box.com', CreateWebLinkParent(id=parent.id), name=get_uuid(), description='Weblink description')
```

### Arguments

- url `str`
  - The URL that this web link links to. Must start with `"http://"` or `"https://"`.
- parent `CreateWebLinkParent`
  - The parent folder to create the web link within.
- name `Optional[str]`
  - Name of the web link. Defaults to the URL if not set.
- description `Optional[str]`
  - Description of the web link.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns the newly created web link object.

## Get web link

Retrieve information about a web link.

This operation is performed by calling function `get_web_link_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-web-links-id/).

<!-- sample get_web_links_id -->

```python
client.web_links.get_web_link_by_id(weblink.id)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- boxapi `Optional[str]`
  - The URL, and optional password, for the shared link of this item. This header can be used to access items that have not been explicitly shared with a user. Use the format `shared_link=[link]` or if a password is required then use `shared_link=[link]&shared_link_password=[password]`. This header can be used on the file or folder shared, as well as on any files or folders nested within the item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns the web link object.

## Update web link

Updates a web link object.

This operation is performed by calling function `update_web_link_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-web-links-id/).

<!-- sample put_web_links_id -->

```python
client.web_links.update_web_link_by_id(weblink.id, name=updated_name, shared_link=UpdateWebLinkByIdSharedLink(access=UpdateWebLinkByIdSharedLinkAccessField.OPEN, password=password))
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- url `Optional[str]`
  - The new URL that the web link links to. Must start with `"http://"` or `"https://"`.
- parent `Optional[UpdateWebLinkByIdParent]`
- name `Optional[str]`
  - A new name for the web link. Defaults to the URL if not set.
- description `Optional[str]`
  - A new description of the web link.
- shared_link `Optional[UpdateWebLinkByIdSharedLink]`
  - The settings for the shared link to update.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns the updated web link object.

## Remove web link

Deletes a web link.

This operation is performed by calling function `delete_web_link_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-web-links-id/).

<!-- sample delete_web_links_id -->

```python
client.web_links.delete_web_link_by_id(web_link_id)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

An empty response will be returned when the web link
was successfully deleted.
