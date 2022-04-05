Configuration
=============

The Python SDK has helpful custom config that you can set for a variety of use cases.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Proxy](#proxy)
  - [Unauthenticated Proxy](#unauthenticated-proxy)
  - [Basic Authentication Proxy](#basic-authentication-proxy)
- [Dafault URLs](#dafault-urls)
  - [Base URL](#base-url)
  - [OAUTH2 URLs](#oauth2-urls)
  - [Upload URL](#upload-url)
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

The Python SDK also lets you set an authenticated proxy. To do this, specify the `user` and `password` fields and pass set that on the `Proxy.AUTH` field.

```python
from boxsdk.config import Proxy
Proxy.AUTH = {
    'user': 'test_user',
    'password': 'test_password',
}
```

Dafault URLs
------------

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
API.OAUTH2_AUTHORIZE_URL = 'https://my-company/authorize'
```

### Upload URL
The default URL used when uploading files to Box can be changed by assigning a new value to the `API.UPLOAD_URL` field.

```python
from boxsdk.config import API
API.UPLOAD_URL = 'https://my-company-upload-url.com'
```

Max retry attmepts
------------------

The default maximum number of retries in case of failed API call is 5 (usually 202, 429 and >= 500 response codes are retried).
To change this number you can set `API.MAX_RETRY_ATTEMPTS` field.
```python
from boxsdk.config import API
API.MAX_RETRY_ATTEMPTS = 6
```
