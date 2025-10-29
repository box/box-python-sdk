# EnterpriseConfigurationsManager

- [Get enterprise configuration](#get-enterprise-configuration)

## Get enterprise configuration

Retrieves the configuration for an enterprise.

This operation is performed by calling function `get_enterprise_configuration_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-enterprise-configurations-id/).

<!-- sample get_enterprise_configurations_id_v2025.0 -->

```python
admin_client.enterprise_configurations.get_enterprise_configuration_by_id_v2025_r0(
    enterprise_id, ["user_settings", "content_and_sharing", "security", "shield"]
)
```

### Arguments

- enterprise_id `str`
  - The ID of the enterprise. Example: "3442311"
- categories `List[str]`
  - A comma-separated list of the enterprise configuration categories. Allowed values: `security`, `content_and_sharing`, `user_settings`, `shield`.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `EnterpriseConfigurationV2025R0`.

Returns the enterprise configuration.
