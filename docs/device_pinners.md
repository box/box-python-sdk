# DevicePinnersManager

- [Get device pin](#get-device-pin)
- [Remove device pin](#remove-device-pin)
- [List enterprise device pins](#list-enterprise-device-pins)

## Get device pin

Retrieves information about an individual device pin.

This operation is performed by calling function `get_device_pinner_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-device-pinners-id/).

<!-- sample get_device_pinners_id -->

```python
client.device_pinners.get_device_pinner_by_id(device_pinner_id)
```

### Arguments

- device_pinner_id `str`
  - The ID of the device pin. Example: "2324234"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DevicePinner`.

Returns information about a single device pin.

## Remove device pin

Deletes an individual device pin.

This operation is performed by calling function `delete_device_pinner_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-device-pinners-id/).

<!-- sample delete_device_pinners_id -->

```python
client.device_pinners.delete_device_pinner_by_id(device_pinner_id)
```

### Arguments

- device_pinner_id `str`
  - The ID of the device pin. Example: "2324234"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the pin has been deleted.

## List enterprise device pins

Retrieves all the device pins within an enterprise.

The user must have admin privileges, and the application
needs the "manage enterprise" scope to make this call.

This operation is performed by calling function `get_enterprise_device_pinners`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-enterprises-id-device-pinners/).

<!-- sample get_enterprises_id_device_pinners -->

```python
client.device_pinners.get_enterprise_device_pinners(enterprise_id)
```

### Arguments

- enterprise_id `str`
  - The ID of the enterprise. Example: "3442311"
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- direction `Optional[GetEnterpriseDevicePinnersDirection]`
  - The direction to sort results in. This can be either in alphabetical ascending (`ASC`) or descending (`DESC`) order.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DevicePinners`.

Returns a list of device pins for a given enterprise.
