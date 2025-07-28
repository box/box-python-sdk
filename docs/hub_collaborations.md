# HubCollaborationsManager

- [Get hub collaborations](#get-hub-collaborations)
- [Create hub collaboration](#create-hub-collaboration)
- [Get hub collaboration by collaboration ID](#get-hub-collaboration-by-collaboration-id)
- [Update hub collaboration](#update-hub-collaboration)
- [Remove hub collaboration](#remove-hub-collaboration)

## Get hub collaborations

Retrieves all collaborations for a hub.

This operation is performed by calling function `get_hub_collaborations_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-hub-collaborations/).

<!-- sample get_hub_collaborations_v2025.0 -->

```python
client.hub_collaborations.get_hub_collaborations_v2025_r0(hub.id)
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

This function returns a value of type `HubCollaborationsV2025R0`.

Retrieves the collaborations associated with the specified hub.

## Create hub collaboration

Adds a collaboration for a single user or a single group to a hub.

Collaborations can be created using email address, user IDs, or group IDs.

This operation is performed by calling function `create_hub_collaboration_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-hub-collaborations/).

<!-- sample post_hub_collaborations_v2025.0 -->

```python
client.hub_collaborations.create_hub_collaboration_v2025_r0(
    CreateHubCollaborationV2025R0Hub(id=hub.id),
    CreateHubCollaborationV2025R0AccessibleBy(type="user", id=user.id),
    "viewer",
)
```

### Arguments

- hub `CreateHubCollaborationV2025R0Hub`
  - Hubs reference.
- accessible_by `CreateHubCollaborationV2025R0AccessibleBy`
  - The user or group who gets access to the item.
- role `str`
  - The level of access granted to hub. Possible values are `editor`, `viewer`, and `co-owner`.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubCollaborationV2025R0`.

Returns a new hub collaboration object.

## Get hub collaboration by collaboration ID

Retrieves details for a hub collaboration by collaboration ID.

This operation is performed by calling function `get_hub_collaboration_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-hub-collaborations-id/).

<!-- sample get_hub_collaborations_id_v2025.0 -->

```python
client.hub_collaborations.get_hub_collaboration_by_id_v2025_r0(created_collaboration.id)
```

### Arguments

- hub_collaboration_id `str`
  - The ID of the hub collaboration. Example: "1234"
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubCollaborationV2025R0`.

Returns a hub collaboration object.

## Update hub collaboration

Updates a hub collaboration.
Can be used to change the hub role.

This operation is performed by calling function `update_hub_collaboration_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/put-hub-collaborations-id/).

<!-- sample put_hub_collaborations_id_v2025.0 -->

```python
client.hub_collaborations.update_hub_collaboration_by_id_v2025_r0(
    created_collaboration.id, role="editor"
)
```

### Arguments

- hub_collaboration_id `str`
  - The ID of the hub collaboration. Example: "1234"
- role `Optional[str]`
  - The level of access granted to hub. Possible values are `editor`, `viewer`, and `co-owner`.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubCollaborationV2025R0`.

Returns an updated hub collaboration object.

## Remove hub collaboration

Deletes a single hub collaboration.

This operation is performed by calling function `delete_hub_collaboration_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/delete-hub-collaborations-id/).

<!-- sample delete_hub_collaborations_id_v2025.0 -->

```python
client.hub_collaborations.delete_hub_collaboration_by_id_v2025_r0(
    created_collaboration.id
)
```

### Arguments

- hub_collaboration_id `str`
  - The ID of the hub collaboration. Example: "1234"
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

A blank response is returned if the hub collaboration was
successfully deleted.
