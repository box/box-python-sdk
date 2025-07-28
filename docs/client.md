# Client

This is the central entrypoint for all SDK interaction. The BoxClient houses all the API endpoints
divided across resource managers.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Make custom HTTP request](#make-custom-http-request)
  - [JSON request](#json-request)
  - [Multi-part request](#multi-part-request)
  - [Binary response](#binary-response)
- [Additional headers](#additional-headers)
  - [As-User header](#as-user-header)
  - [Suppress notifications](#suppress-notifications)
  - [Custom headers](#custom-headers)
- [Custom Base URLs](#custom-base-urls)
- [Use Proxy for API calls](#use-proxy-for-api-calls)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Make custom HTTP request

You can make custom HTTP requests using the `client.make_request()` method.
This method allows you to make any HTTP request to the Box API. It will automatically use authentication and
network configuration settings from the client.
The method accepts a `FetchOptions` object as an argument and returns a `FetchResponse` object.

## JSON request

The following example demonstrates how to make a custom POST request to create a new folder in the root folder.

```python
from box_sdk_gen import FetchResponse, FetchOptions

response: FetchResponse = client.make_request(
    FetchOptions(
        method="POST",
        url="https://api.box.com/2.0/folders",
        data={"name": "new_folder_name", "parent": {"id": "0"}},
    )
)
print("Received status code: ", response.status)
print("Created folder name: ", response.data["name"])
```

## Multi-part request

The following example demonstrates how to make a custom multipart request that uploads a file to a folder.

```python
from box_sdk_gen import FetchResponse, FetchOptions, MultipartItem

response: FetchResponse = client.make_request(
    FetchOptions(
        method="POST",
        url="https://upload.box.com/api/2.0/files/content",
        content_type="multipart/form-data",
        multipart_data=[
            MultipartItem(
                part_name="attributes",
                data={"name": "new_folder_name", "parent": {"id": "0"}},
            ),
            MultipartItem(part_name="file", file_stream=open("file.txt", "rb")),
        ],
    )
)
print("Received status code: ", response.status)
```

## Binary response

The following example demonstrates how to make a custom request that expects a binary response.
It is required to specify the `response_format` parameter in the `FetchOptions` object to `ResponseFormat.BINARY`.

```python
from box_sdk_gen import FetchResponse, FetchOptions, ResponseFormat

file_id = "1234567"
response: FetchResponse = client.make_request(
    FetchOptions(
        method="GET",
        url="".join(["https://api.box.com/2.0/files/", file_id, "/content"]),
        response_format=ResponseFormat.BINARY,
    )
)
print("Received status code: ", response.status)
with open("file.txt", "wb") as file:
    file.write(response.content)
```

# Additional headers

BoxClient provides a convenient methods, which allow passing additional headers, which will be included
in every API call made by the client.

## As-User header

The As-User header is used by enterprise admins to make API calls on behalf of their enterprise's users.
This requires the API request to pass an As-User: USER-ID header. For more details see the [documentation on As-User](https://developer.box.com/en/guides/authentication/oauth2/as-user/).

The following example assume that the client has been instantiated with an access token belonging to an admin-level user
or Service Account with appropriate privileges to make As-User calls.

Calling the `client.with_as_user_header()` method creates a new client to impersonate user with the provided ID.
All calls made with the new client will be made in context of the impersonated user, leaving the original client unmodified.

<!-- sample x_auth init_with_as_user_header -->

```python
user_client = client.with_as_user_header(user_id="1234567")
```

## Suppress notifications

If you are making administrative API calls (that is, your application has “Manage an Enterprise”
scope, and the user signing in is a co-admin with the correct "Edit settings for your company"
permission) then you can suppress both email and webhook notifications. This can be used, for
example, for a virus-scanning tool to download copies of everyone’s files in an enterprise,
without every collaborator on the file getting an email. All actions will still appear in users'
updates feed and audit logs.

> **Note:** This functionality is only available for approved applications.

Calling the `client.with_suppressed_notifications()` method creates a new client.
For all calls made with the new client the notifications will be suppressed.

```python
new_client = client.with_suppressed_notifications()
```

## Custom headers

You can also specify the custom set of headers, which will be included in every API call made by client.
Calling the `client.with_extra_headers()` method creates a new client, leaving the original client unmodified.

```python
new_client = client.with_extra_headers(extra_headers={"customHeader": "customValue"})
```

# Custom Base URLs

You can also specify the custom base URLs, which will be used for API calls made by client.
Calling the `client.with_custom_base_urls()` method creates a new client, leaving the original client unmodified.

```python
new_client = client.with_custom_base_urls(
    base_urls=BaseUrls(
        base_url="https://api.box.com",
        upload_url="https://upload.box.com/api",
        oauth_2_url="https://account.box.com/api/oauth2",
    )
)
```

# Use Proxy for API calls

In order to use a proxy for API calls, calling the `client.with_proxy(proxyConfig)` method creates a new client, leaving the original client unmodified, with the username and password being optional.

**Note:** We are only supporting http/s proxies with basic authentication. NTLM and other authentication methods are not supported.

```python
new_client = client.with_proxy(
    ProxyConfig(url="http://proxy.com", username="username", password="password")
)
```
