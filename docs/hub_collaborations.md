# HubCollaborationsManager

- [Get Box Hub collaborations](#get-box-hub-collaborations)
- [Create Box Hub collaboration](#create-box-hub-collaboration)
- [Get Box Hub collaboration by collaboration ID](#get-box-hub-collaboration-by-collaboration-id)
- [Update Box Hub collaboration](#update-box-hub-collaboration)
- [Remove Box Hub collaboration](#remove-box-hub-collaboration)

## Get Box Hub collaborations

Retrieves all collaborations for a Box Hub.

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

Retrieves the collaborations associated with the specified Box Hub.

## Create Box Hub collaboration

Adds a collaboration for a single user or a single group to a Box Hub.

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
  - Box Hubs reference.
- accessible_by `CreateHubCollaborationV2025R0AccessibleBy`
  - The user or group who gets access to the item.
- role `str`
  - The level of access granted to a Box Hub. Possible values are `editor`, `viewer`, and `co-owner`.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubCollaborationV2025R0`.

Returns a new Box Hub collaboration object.

## Get Box Hub collaboration by collaboration ID

Retrieves details for a Box Hub collaboration by collaboration ID.

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

Returns a Box Hub collaboration object.

## Update Box Hub collaboration

Updates a Box Hub collaboration.
Can be used to change the Box Hub role.

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
  - The level of access granted to a Box Hub. Possible values are `editor`, `viewer`, and `co-owner`.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `HubCollaborationV2025R0`.

Returns an updated Box Hub collaboration object.

## Remove Box Hub collaboration

Deletes a single Box Hub collaboration.

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

A blank response is returned if the Box Hub collaboration was
successfully deleted.
