# HubItemsManager

- [Get hub items](#get-hub-items)
- [Manage hub items](#manage-hub-items)

## Get hub items

Retrieves all items associated with a Hub.

This operation is performed by calling function `get_hub_items_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-hub-items/).

<!-- sample get_hub_items_v2025.0 -->

```python
client.hub_items.get_hub_items_v2025_r0(created_hub.id)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubItemsV2025R0`.

Retrieves the items associated with the specified Hub.

## Manage hub items

Adds and/or removes Hub items from a Hub.

This operation is performed by calling function `manage_hub_items_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-hubs-id-manage-items/).

<!-- sample post_hubs_id_manage_items_v2025.0 -->

```python
client.hub_items.manage_hub_items_v2025_r0(
    created_hub.id,
    operations=[
        HubItemOperationV2025R0(
            action=HubItemOperationV2025R0ActionField.ADD,
            item=FolderReferenceV2025R0(id=folder.id),
        )
    ],
)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`. Example: "12345"
- operations `Optional[List[HubItemOperationV2025R0]]`
  - List of operations to perform on Hub items.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubItemsManageResponseV2025R0`.
