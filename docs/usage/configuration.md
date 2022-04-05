Configuration
=============

The Python SDK has helpful custom config that you can set for a variety of use cases.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Proxy](#proxy)
  - [Unauthenticated Proxy](#unauthenticated-proxy)
  - [Basic Authentication Proxy](#basic-authentication-proxy)
- [Base url](#base-url)
- [Max retry attmepts](#max-retry-attmepts)

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

Base url
--------

The default base url used for making API calls to Box can be changed by setting the value of the `API.BASE_API_URL` field.

```python
from boxsdk.config import API
API.BASE_API_URL = 'https://new-base-url.com'
```

Max retry attmepts
------------------

The default maximum number of retries in case of failed API call is 5 (usually 202, 429 and >= 500 response codes are retried).
To change this number you can set `API.MAX_RETRY_ATTEMPTS` field.
```python
from boxsdk.config import API
API.MAX_RETRY_ATTEMPTS = 6
```
