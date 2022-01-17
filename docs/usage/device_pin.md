Device Pins
===========

Device pinning is a feature that allows enterprise admins to pin their user’s
corporate-managed Box account to a particular mobile device or Box Sync client.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [List Enterprise Device Pins](#list-enterprise-device-pins)
- [Get Device Pin Information](#get-device-pin-information)
- [Delete Device Pin](#delete-device-pin)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Enterprise Device Pins
---------------------------

To retrieve all device pins for an enterprise, call
[`client.device_pinners(enterprise=None, limit=None, marker=None, direction=None, fields=None)`][device_pinners].
If an `enterprise` is not specified, this defaults to the current enterprise.  This method returns a
`BoxObjectCollection` that allows you to iterate over the [`DevicePinner`][device_pin_class] objects in the collection.

<!-- sample get_enterprises_id_device_pinners -->
```python
device_pins = client.device_pinners()
for pin in device_pins:
    print(f'Pinned {pin.product_name} device for {pin.owned_by.name}')
```

[device_pinners]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.device_pinners
[device_pin_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.device_pinner.DevicePinner

Get Device Pin Information
--------------------------

To get information about a specific device pin, call [`device_pinner.get(*, fields=None, headers=None, **kwargs)`][get].
This method returns a new [`DevicePinner`][device_pin_class] object with fields populated by data from the API.

<!-- sample get_device_pinners_id -->
```python
device_pin_id = '1111'
device_pin = client.device_pinner(device_pin_id).get()
print(f'{pin.product_name} device for {pin.owned_by.name} is pinned')
```

[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Delete Device Pin
-----------------

To delete a specific device pin, call [`device_pinner.delete()`][delete].  This method returns `True` to indicate that
the deletion was successful.

<!-- sample delete_device_pinners_id -->
```python
device_pin_id = '1111'
client.device_pin(device_pin_id).delete()
print('Device pin deleted!')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete
