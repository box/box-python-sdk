# HubsManager

- [List all hubs](#list-all-hubs)
- [Create hub](#create-hub)
- [List all hubs for requesting enterprise](#list-all-hubs-for-requesting-enterprise)
- [Get hub information by ID](#get-hub-information-by-id)
- [Update hub information by ID](#update-hub-information-by-id)
- [Delete hub](#delete-hub)
- [Copy hub](#copy-hub)

## List all hubs

Retrieves all hubs for requesting user.

This operation is performed by calling function `get_hubs_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-hubs/).

<!-- sample get_hubs_v2025.0 -->

```python
client.hubs.get_hubs_v2025_r0(
    scope="all", sort="name", direction=GetHubsV2025R0Direction.ASC
)
```

### Arguments

- query `Optional[str]`
  - The query string to search for hubs.
- scope `Optional[str]`
  - The scope of the hubs to retrieve. Possible values include `editable`, `view_only`, and `all`. Default is `all`.
- sort `Optional[str]`
  - The field to sort results by. Possible values include `name`, `updated_at`, `last_accessed_at`, `view_count`, and `relevance`. Default is `relevance`.
- direction `Optional[GetHubsV2025R0Direction]`
  - The direction to sort results in. This can be either in alphabetical ascending (`ASC`) or descending (`DESC`) order.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubsV2025R0`.

Returns all hubs for the given user or enterprise.

## Create hub

Creates a new Hub.

This operation is performed by calling function `create_hub_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-hubs/).

<!-- sample post_hubs_v2025.0 -->

```python
client.hubs.create_hub_v2025_r0(hub_title, description=hub_description)
```

### Arguments

- title `str`
  - Title of the Hub. It cannot be empty and should be less than 50 characters.
- description `Optional[str]`
  - Description of the Hub.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubV2025R0`.

Returns a new Hub object.

## List all hubs for requesting enterprise

Retrieves all hubs for a given enterprise.

Admins or Hub Co-admins of an enterprise
with GCM scope can make this call.

This operation is performed by calling function `get_enterprise_hubs_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-enterprise-hubs/).

<!-- sample get_enterprise_hubs_v2025.0 -->

```python
client.hubs.get_enterprise_hubs_v2025_r0(
    sort="name", direction=GetEnterpriseHubsV2025R0Direction.ASC
)
```

### Arguments

- query `Optional[str]`
  - The query string to search for hubs.
- sort `Optional[str]`
  - The field to sort results by. Possible values include `name`, `updated_at`, `last_accessed_at`, `view_count`, and `relevance`. Default is `relevance`.
- direction `Optional[GetEnterpriseHubsV2025R0Direction]`
  - The direction to sort results in. This can be either in alphabetical ascending (`ASC`) or descending (`DESC`) order.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubsV2025R0`.

Returns all hubs for the given user or enterprise.

## Get hub information by ID

Retrieves details for a hub by its ID.

This operation is performed by calling function `get_hub_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-hubs-id/).

<!-- sample get_hubs_id_v2025.0 -->

```python
client.hubs.get_hub_by_id_v2025_r0(hub_id)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`. Example: "12345"
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubV2025R0`.

Returns a hub object.

## Update hub information by ID

Updates a Hub. Can be used to change title, description, or Hub settings.

This operation is performed by calling function `update_hub_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/put-hubs-id/).

<!-- sample put_hubs_id_v2025.0 -->

```python
client.hubs.update_hub_by_id_v2025_r0(
    hub_id, title=new_hub_title, description=new_hub_description
)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`. Example: "12345"
- title `Optional[str]`
  - Title of the Hub. It cannot be empty and should be less than 50 characters.
- description `Optional[str]`
  - Description of the Hub.
- is_ai_enabled `Optional[bool]`
  - Indicates if AI features are enabled for the Hub.
- is_collaboration_restricted_to_enterprise `Optional[bool]`
  - Indicates if collaboration is restricted to the enterprise.
- can_non_owners_invite `Optional[bool]`
  - Indicates if non-owners can invite others to the Hub.
- can_shared_link_be_created `Optional[bool]`
  - Indicates if a shared link can be created for the Hub.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubV2025R0`.

Returns a Hub object.

## Delete hub

Deletes a single hub.

This operation is performed by calling function `delete_hub_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/delete-hubs-id/).

<!-- sample delete_hubs_id_v2025.0 -->

```python
client.hubs.delete_hub_by_id_v2025_r0(hub_id)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`. Example: "12345"
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the hub was
successfully deleted.

## Copy hub

Creates a copy of a Hub.

The original Hub will not be modified.

This operation is performed by calling function `copy_hub_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-hubs-id-copy/).

<!-- sample post_hubs_id_copy_v2025.0 -->

```python
client.hubs.copy_hub_v2025_r0(
    created_hub.id, title=copied_hub_title, description=copied_hub_description
)
```

### Arguments

- hub_id `str`
  - The unique identifier that represent a hub. The ID for any hub can be determined by visiting this hub in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/hubs/123` the `hub_id` is `123`. Example: "12345"
- title `Optional[str]`
  - Title of the Hub. It cannot be empty and should be less than 50 characters.
- description `Optional[str]`
  - Description of the Hub.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubV2025R0`.

Returns a new Hub object.
