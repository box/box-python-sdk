# AvatarsManager

- [Get user avatar](#get-user-avatar)
- [Add or update user avatar](#add-or-update-user-avatar)
- [Delete user avatar](#delete-user-avatar)

## Get user avatar

Retrieves an image of a the user's avatar.

This operation is performed by calling function `get_user_avatar`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-users-id-avatar/).

<!-- sample get_users_id_avatar -->

```python
client.avatars.get_user_avatar(user.id)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ByteStream`.

When an avatar can be found for the user the
image data will be returned in the body of the
response.

## Add or update user avatar

Adds or updates a user avatar.

This operation is performed by calling function `create_user_avatar`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-users-id-avatar/).

<!-- sample post_users_id_avatar -->

```python
client.avatars.create_user_avatar(
    user.id,
    decode_base_64_byte_stream(
        "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEAAQMAAABmvDolAAAAA1BMVEW10NBjBBbqAAAAH0lEQVRoge3BAQ0AAADCoPdPbQ43oAAAAAAAAAAAvg0hAAABmmDh1QAAAABJRU5ErkJggg=="
    ),
    pic_file_name="avatar.png",
    pic_content_type="image/png",
)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- pic `ByteStream`
  - The image file to be uploaded to Box. Accepted file extensions are `.jpg` or `.png`. The maximum file size is 1MB.
- pic_file_name `Optional[str]`
- pic_content_type `Optional[str]`
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `UserAvatar`.

`ok`: Returns the `pic_urls` object with URLs to existing
user avatars that were updated.`created`: Returns the `pic_urls` object with URLS to user avatars
uploaded to Box with the request.

## Delete user avatar

Removes an existing user avatar.
You cannot reverse this operation.

This operation is performed by calling function `delete_user_avatar`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-users-id-avatar/).

<!-- sample delete_users_id_avatar -->

```python
client.avatars.delete_user_avatar(user.id)
```

### Arguments

- user_id `str`
  - The ID of the user. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

`no_content`: Removes the avatar and returns an empty response.
