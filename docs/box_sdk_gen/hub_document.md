# HubDocumentManager

- [List Hub Document Pages](#list-hub-document-pages)
- [List Hub Document blocks for page](#list-hub-document-blocks-for-page)

## List Hub Document Pages

Retrieves a list of Hub Document Pages for the specified hub.
Includes both root-level pages and sub pages.

This operation is performed by calling function `get_hub_document_pages_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-hub-document-pages/).

<!-- sample get_hub_document_pages_v2025.0 -->

```python
client.hub_document.get_hub_document_pages_v2025_r0(hub_id)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubDocumentPagesV2025R0`.

Returns a Hub Document Pages response whose `entries` array contains root-level pages and sub pages. Includes pagination when more results are available.

## List Hub Document blocks for page

Retrieves a sorted list of all Hub Document Blocks on a specified page in the hub document, excluding items.
Blocks are hierarchically organized by their `parent_id`.
Blocks are sorted in order based on user specification in the user interface.
The response will only include content blocks that belong to the specified page. This will not include sub pages or sub page content blocks.

This operation is performed by calling function `get_hub_document_blocks_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-hub-document-blocks/).

<!-- sample get_hub_document_blocks_v2025.0 -->

```python
client.hub_document.get_hub_document_blocks_v2025_r0(hub_id, page_id)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`.
- page_id `str`
  - The unique identifier of a page within the Box Hub.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubDocumentBlocksV2025R0`.

Returns a Hub Document Blocks response whose `entries` array contains all content blocks of the specified page, except for items.
To retrieve items, use the `GET /hub_items` endpoint.
