Configuration
=============

The Python SDK has helpful custom config that you can set for a variety of use cases.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Proxy](#proxy)
  - [Unauthenticated Proxy](#unauthenticated-proxy)
  - [Basic Authentication Proxy](#basic-authentication-proxy)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Proxy
-----

### Unauthenticated Proxy

In order to set up configuration for basic proxy with the Python SDK, simply specify the proxy address for the `Proxy.URL` field.

```python
from boxsdk.config import Proxy
Proxy.URL = 'http://example-proxy-address.com'
```

### Basic Authentication Proxy

The Python SDK also lets you set an authenticated proxy. To do this specify the `user` and `password` fields and pass set that on the `Proxy.AUTH` field.

```python
from boxsdk.config import Proxy
Proxy.AUTH = {
    'user': 'test_user',
    'password': 'test_password',
}
```

