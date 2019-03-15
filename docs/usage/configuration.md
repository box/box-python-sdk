Configuration
=============

The Python SDK has helpful custom config that you can set for a variety of use cases.

Proxy
-----

### Basic Authentication

In order to set up configuration for basic proxy with the Python SDK, simply specify the proxy address for the `PROXY.URL` field.

```python
from boxsdk.config import PROXY
PROXY.URL = 'http://example-proxy-address.com'
```

### Authenticated Proxy

The Python SDK also lets you set an authenticated proxy. To do this specify the `user` and `password` fields and pass set that on the `PROXY.AUTH` field.

```python
from boxsdk.config import PROXY
PROXY.AUTH = {
    'user': 'test_user',
    'password': 'test_password',
}
```

