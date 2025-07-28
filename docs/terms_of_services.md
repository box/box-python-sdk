# TermsOfServicesManager

- [List terms of services](#list-terms-of-services)
- [Create terms of service](#create-terms-of-service)
- [Get terms of service](#get-terms-of-service)
- [Update terms of service](#update-terms-of-service)

## List terms of services

Returns the current terms of service text and settings
for the enterprise.

This operation is performed by calling function `get_terms_of_service`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-terms-of-services/).

<!-- sample get_terms_of_services -->

```python
client.terms_of_services.get_terms_of_service()
```

### Arguments

- tos_type `Optional[GetTermsOfServiceTosType]`
  - Limits the results to the terms of service of the given type.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TermsOfServices`.

Returns a collection of terms of service text and settings for the
enterprise.

## Create terms of service

Creates a terms of service for a given enterprise
and type of user.

This operation is performed by calling function `create_terms_of_service`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-terms-of-services/).

<!-- sample post_terms_of_services -->

```python
client.terms_of_services.create_terms_of_service(
    CreateTermsOfServiceStatus.DISABLED,
    "Test TOS",
    tos_type=CreateTermsOfServiceTosType.MANAGED,
)
```

### Arguments

- status `CreateTermsOfServiceStatus`
  - Whether this terms of service is active.
- tos_type `Optional[CreateTermsOfServiceTosType]`
  - The type of user to set the terms of service for.
- text `str`
  - The terms of service text to display to users. The text can be set to empty if the `status` is set to `disabled`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TermsOfService`.

Returns a new task object.

## Get terms of service

Fetches a specific terms of service.

This operation is performed by calling function `get_terms_of_service_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-terms-of-services-id/).

_Currently we don't have an example for calling `get_terms_of_service_by_id` in integration tests_

### Arguments

- terms_of_service_id `str`
  - The ID of the terms of service. Example: "324234"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TermsOfService`.

Returns a terms of service object.

## Update terms of service

Updates a specific terms of service.

This operation is performed by calling function `update_terms_of_service_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-terms-of-services-id/).

<!-- sample put_terms_of_services_id -->

```python
client.terms_of_services.update_terms_of_service_by_id(
    tos.id, UpdateTermsOfServiceByIdStatus.DISABLED, "TOS"
)
```

### Arguments

- terms_of_service_id `str`
  - The ID of the terms of service. Example: "324234"
- status `UpdateTermsOfServiceByIdStatus`
  - Whether this terms of service is active.
- text `str`
  - The terms of service text to display to users. The text can be set to empty if the `status` is set to `disabled`.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `TermsOfService`.

Returns an updated terms of service object.
