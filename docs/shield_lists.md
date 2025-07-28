# ShieldListsManager

- [Get all shield lists in enterprise](#get-all-shield-lists-in-enterprise)
- [Create shield list](#create-shield-list)
- [Get single shield list by shield list id](#get-single-shield-list-by-shield-list-id)
- [Delete single shield list by shield list id](#delete-single-shield-list-by-shield-list-id)
- [Update shield list](#update-shield-list)

## Get all shield lists in enterprise

Retrieves all shield lists in the enterprise.

This operation is performed by calling function `get_shield_lists_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-shield-lists/).

<!-- sample get_shield_lists_v2025.0 -->

```python
client.shield_lists.get_shield_lists_v2025_r0()
```

### Arguments

- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldListsV2025R0`.

Returns the list of shield list objects.

## Create shield list

Creates a shield list.

This operation is performed by calling function `create_shield_list_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-shield-lists/).

<!-- sample post_shield_lists_v2025.0 -->

```python
client.shield_lists.create_shield_list_v2025_r0(
    shield_list_country_name,
    ShieldListContentCountryV2025R0(
        type=ShieldListContentCountryV2025R0TypeField.COUNTRY,
        country_codes=["US", "PL"],
    ),
    description="A list of things that are shielded",
)
```

### Arguments

- name `str`
  - The name of the shield list.
- description `Optional[str]`
  - Optional description of Shield List.
- content `ShieldListContentRequestV2025R0`
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldListV2025R0`.

Returns the shield list object.

## Get single shield list by shield list id

Retrieves a single shield list by its ID.

This operation is performed by calling function `get_shield_list_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-shield-lists-id/).

<!-- sample get_shield_lists_id_v2025.0 -->

```python
client.shield_lists.get_shield_list_by_id_v2025_r0(shield_list_country.id)
```

### Arguments

- shield_list_id `str`
  - The unique identifier that represents a shield list. The ID for any Shield List can be determined by the response from the endpoint fetching all shield lists for the enterprise. Example: "90fb0e17-c332-40ed-b4f9-fa8908fbbb24 "
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldListV2025R0`.

Returns the shield list object.

## Delete single shield list by shield list id

Delete a single shield list by its ID.

This operation is performed by calling function `delete_shield_list_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/delete-shield-lists-id/).

<!-- sample delete_shield_lists_id_v2025.0 -->

```python
client.shield_lists.delete_shield_list_by_id_v2025_r0(shield_list_country.id)
```

### Arguments

- shield_list_id `str`
  - The unique identifier that represents a shield list. The ID for any Shield List can be determined by the response from the endpoint fetching all shield lists for the enterprise. Example: "90fb0e17-c332-40ed-b4f9-fa8908fbbb24 "
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Shield List correctly removed. No content in response.

## Update shield list

Updates a shield list.

This operation is performed by calling function `update_shield_list_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/put-shield-lists-id/).

<!-- sample put_shield_lists_id_v2025.0 -->

```python
client.shield_lists.update_shield_list_by_id_v2025_r0(
    shield_list_country.id,
    shield_list_country_name,
    ShieldListContentCountryV2025R0(
        type=ShieldListContentCountryV2025R0TypeField.COUNTRY, country_codes=["US"]
    ),
    description="Updated description",
)
```

### Arguments

- shield_list_id `str`
  - The unique identifier that represents a shield list. The ID for any Shield List can be determined by the response from the endpoint fetching all shield lists for the enterprise. Example: "90fb0e17-c332-40ed-b4f9-fa8908fbbb24 "
- name `str`
  - The name of the shield list.
- description `Optional[str]`
  - Optional description of Shield List.
- content `ShieldListContentRequestV2025R0`
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `ShieldListV2025R0`.

Returns the shield list object.
