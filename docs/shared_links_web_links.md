# SharedLinksWebLinksManager

- [Find web link for shared link](#find-web-link-for-shared-link)
- [Get shared link for web link](#get-shared-link-for-web-link)
- [Add shared link to web link](#add-shared-link-to-web-link)
- [Update shared link on web link](#update-shared-link-on-web-link)
- [Remove shared link from web link](#remove-shared-link-from-web-link)

## Find web link for shared link

Returns the web link represented by a shared link.

A shared web link can be represented by a shared link,
which can originate within the current enterprise or within another.

This endpoint allows an application to retrieve information about a
shared web link when only given a shared link.

This operation is performed by calling function `find_web_link_for_shared_link`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-shared-items--web-links/).

<!-- sample get_shared_items#web_links -->

```python
user_client.shared_links_web_links.find_web_link_for_shared_link(
    "".join(
        [
            "shared_link=",
            web_link_from_api.shared_link.url,
            "&shared_link_password=Secret123@",
        ]
    )
)
```

### Arguments

- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- if_none_match `Optional[str]`
  - Ensures an item is only returned if it has changed. Pass in the item's last observed `etag` value into this header and the endpoint will fail with a `304 Not Modified` if the item has not changed since.
- boxapi `str`
  - A header containing the shared link and optional password for the shared link. The format for this header is as follows: `shared_link=[link]&shared_link_password=[password]`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns a full web link resource if the shared link is valid and
the user has access to it.

## Get shared link for web link

Gets the information for a shared link on a web link.

This operation is performed by calling function `get_shared_link_for_web_link`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-web-links-id--get-shared-link/).

<!-- sample get_web_links_id#get_shared_link -->

```python
client.shared_links_web_links.get_shared_link_for_web_link(web_link_id, "shared_link")
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns the base representation of a web link with the
additional shared link information.

## Add shared link to web link

Adds a shared link to a web link.

This operation is performed by calling function `add_share_link_to_web_link`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-web-links-id--add-shared-link/).

<!-- sample put_web_links_id#add_shared_link -->

```python
client.shared_links_web_links.add_share_link_to_web_link(
    web_link_id,
    "shared_link",
    shared_link=AddShareLinkToWebLinkSharedLink(
        access=AddShareLinkToWebLinkSharedLinkAccessField.OPEN, password="Secret123@"
    ),
)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- shared_link `Optional[AddShareLinkToWebLinkSharedLink]`
  - The settings for the shared link to create on the web link. Use an empty object (`{}`) to use the default settings for shared links.
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns the base representation of a web link with a new shared
link attached.

## Update shared link on web link

Updates a shared link on a web link.

This operation is performed by calling function `update_shared_link_on_web_link`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-web-links-id--update-shared-link/).

<!-- sample put_web_links_id#update_shared_link -->

```python
client.shared_links_web_links.update_shared_link_on_web_link(
    web_link_id,
    "shared_link",
    shared_link=UpdateSharedLinkOnWebLinkSharedLink(
        access=UpdateSharedLinkOnWebLinkSharedLinkAccessField.COLLABORATORS
    ),
)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- shared_link `Optional[UpdateSharedLinkOnWebLinkSharedLink]`
  - The settings for the shared link to update.
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns a basic representation of the web link, with the updated shared
link attached.

## Remove shared link from web link

Removes a shared link from a web link.

This operation is performed by calling function `remove_shared_link_from_web_link`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-web-links-id--remove-shared-link/).

<!-- sample put_web_links_id#remove_shared_link -->

```python
client.shared_links_web_links.remove_shared_link_from_web_link(
    web_link_id, "shared_link", shared_link=create_null()
)
```

### Arguments

- web_link_id `str`
  - The ID of the web link. Example: "12345"
- shared_link `Optional[RemoveSharedLinkFromWebLinkSharedLink]`
  - By setting this value to `null`, the shared link is removed from the web link.
- fields `str`
  - Explicitly request the `shared_link` fields to be returned for this item.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `WebLink`.

Returns a basic representation of a web link, with the
shared link removed.
