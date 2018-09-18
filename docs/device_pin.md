Devices
======

Device pinning is a feature that allows enterprise admins to pin their user’s
corporate-managed Box account to a particular mobile device or Box Sync client.


List Enterprise Device Pins
---------------------------

To retrieve all device pins for the enterprise, use `client.device_pinners(enterprise_id, limit=None, marker=None, direction=None, fields=None)`.

```python
enterprise_id = '1234'
device_pins = client.device_pinners(enterprise_id)
for device_in in device_pins:
    # Do something
```

Get Device Pin Information
--------------------------

To get information about a specific device pin. use `device_pin.get()`

```python
device_pin_id = '1111'
device_pin_info = client.device_pinner(device_pin_id).get()
```

Delete Device Pin
-----------------

To delete a specific device pin, use `device_pinner.delete()`

```python
device_pin_id = '1111'
client.device_pin(device_pin_id).delete()
```
