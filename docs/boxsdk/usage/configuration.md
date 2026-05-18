# Configuration

The Python SDK has helpful custom config that you can set for a variety of use cases.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Proxy](#proxy)
  - [Unauthenticated Proxy](#unauthenticated-proxy)
  - [Basic Authentication Proxy](#basic-authentication-proxy)
- [Configure URLs](#configure-urls)
  - [Base URL](#base-url)
  - [OAUTH2 URLs](#oauth2-urls)
  - [Upload URL](#upload-url)
- [Network timeouts](#network-timeouts)
  - [Default behavior](#default-behavior)
  - [Session-wide timeouts](#session-wide-timeouts)
  - [Per-request timeouts](#per-request-timeouts)
  - [Complete example](#complete-example)
- [Max retry attmepts](#max-retry-attmepts)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Proxy

### Unauthenticated Proxy

In order to set up configuration for basic proxy with the Python SDK, simply specify the proxy address for the `Proxy.URL` field.

```python
from boxsdk.config import Proxy
Proxy.URL = 'http://example-proxy-address.com'
```

### Basic Authentication Proxy

The Python SDK also lets you set an authenticated proxy. To do this, specify the `user` and `password` fields and pass set that on the `Proxy.AUTH` field.

```python
from boxsdk.config import Proxy
Proxy.AUTH = {
    'user': 'test_user',
    'password': 'test_password',
}
```

## URLs configuration

### Base URL

The default base URL used for making API calls to Box can be changed by setting the value of the `API.BASE_API_URL` field.

```python
from boxsdk.config import API
API.BASE_API_URL = 'https://new-base-url.com'
```

### OAUTH2 URLs

The default URLs used to authorize a user and obtain OAuth2 authorization tokens can be modified by overwriting
`API.OAUTH2_API_URL` and `API.OAUTH2_AUTHORIZE_URL` constants.

```python
from boxsdk.config import API
API.OAUTH2_API_URL = 'https://my-company.com/oauth2'
API.OAUTH2_AUTHORIZE_URL = 'https://my-company.com/authorize'
```

### Upload URL

The default URL used when uploading files to Box can be changed by assigning a new value to the `API.UPLOAD_URL` field.
If this variable is ever changed from default value, the SDK will alwayse use this URL to upload files to Box,
even if `use_upload_session_urls` is set to `True` while creating an upload session for a chunked upload.

```python
from boxsdk.config import API
API.UPLOAD_URL = 'https://my-company-upload-url.com'
```

## Network timeouts

The legacy **`boxsdk`** package uses the [Requests](https://requests.readthedocs.io/) library for HTTP calls. Timeouts are passed through to `requests` as the `timeout` parameter.

### Default behavior

> **Important:** The legacy SDK does **not** apply default connection or read timeouts. Unless you configure them, Requests uses `timeout=None`, which means the client does not enforce a limit while establishing a connection or while reading the response body.

If your application needs bounded network behavior (recommended for production workloads), you **must** set timeouts explicitly using the options below.

When a timeout is exceeded, the request fails at the HTTP client layer (for example, `requests.exceptions.Timeout`), not as a normal Box API error response with an HTTP status and JSON body.

### Session-wide timeouts

Pass `timeout` in `default_network_request_kwargs` when creating a session, or add it with [`Session.with_default_network_request_kwargs`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.session.html#boxsdk.session.session.Session.with_default_network_request_kwargs) so it applies to every API call on that session.

`timeout` follows the [Requests `timeout` argument](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts): a single number (seconds for connect and read) or a `(connect_timeout, read_timeout)` tuple in seconds.

**New client with timeouts on the session:**

```python
from boxsdk import OAuth2, Client
from boxsdk.session.session import AuthorizedSession

oauth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='YOUR_ACCESS_TOKEN',
)
session = AuthorizedSession(
    oauth,
    default_network_request_kwargs={'timeout': (30.0, 60.0)},  # connect, read (seconds)
)
client = Client(oauth, session=session)
```

**Existing client — clone with an updated session:**

```python
client = Client(oauth)
client = client.clone(
    session=client.session.with_default_network_request_kwargs({'timeout': (30.0, 60.0)})
)
```

### Per-request timeouts

Some API methods accept `extra_network_parameters`, which are merged into the Requests call for that request only (see [`api_call_decorator`](https://github.com/box/box-python-sdk/blob/main/boxsdk/util/api_call_decorator.py)):

```python
folder = client.folder('0').create_subfolder(
    'My Folder',
    extra_network_parameters={'timeout': (30.0, 60.0)},
)
```

### Complete example

```python
from boxsdk import OAuth2, Client
from boxsdk.session.session import AuthorizedSession

oauth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='YOUR_ACCESS_TOKEN',
)
session = AuthorizedSession(
    oauth,
    default_network_request_kwargs={'timeout': 30.0},  # 30s for connect and read
)
client = Client(oauth, session=session)
```

## Max retry attmepts

The default maximum number of retries in case of failed API call is 5 (usually 202, 429 and >= 500 response codes are retried).
To change this number you can set `API.MAX_RETRY_ATTEMPTS` field.

```python
from boxsdk.config import API
API.MAX_RETRY_ATTEMPTS = 6
```
