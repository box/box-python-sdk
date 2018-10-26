Device Pins
===========

Device pinning is a feature that allows enterprise admins to pin their user’s
corporate-managed Box account to a particular mobile device or Box Sync client.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [List Enterprise Device Pins](#list-enterprise-device-pins)
- [Get Device Pin Information](#get-device-pin-information)
- [Delete Device Pin](#delete-device-pin)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

List Enterprise Device Pins
---------------------------

To retrieve all device pins for the enterprise, use `client.device_pinners(enterprise=None, limit=None, marker=None, direction=None, fields=None)`.

```python
device_pins = client.device_pinners()
for device_in in device_pins:
    # Do something
```

Get Device Pin Information
--------------------------

To get information about a specific device pin. use `device_pinner.get()`

```python
device_pin_id = '1111'
device_pin_info = client.device_pinner('device_pin_id).get()
```

Delete Device Pin
-----------------

To delete a specific device pin, use `device_pinner.delete()`

```python
device_pin_id = '1111'
client.device_pin(device_pin_id).delete()
```
