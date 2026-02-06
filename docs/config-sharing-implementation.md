# Configuration Sharing Implementation

This document describes the implementation of configuration sharing between the legacy `boxsdk` package and the new auto-generated `box_sdk_gen` package.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Configuration Sharing Implementation](#configuration-sharing-implementation)
  - [Overview](#overview)
  - [Implementation Components](#implementation-components)
    - [Token Storage Adapter (`boxsdk/util/token_storage_adapter.py`)](#token-storage-adapter-boxsdkutiltoken_storage_adapterpy)
    - [Client Methods](#client-methods)
      - [`get_sdk_gen_client(auth_options=None, network_options=None)`](#get_sdk_gen_clientauth_optionsnone-network_optionsnone)
      - [`get_sdk_gen_authentication(token_storage=None)`](#get_sdk_gen_authenticationtoken_storagenone)
      - [`get_sdk_gen_network_session(**options)`](#get_sdk_gen_network_sessionoptions)
  - [Usage Examples](#usage-examples)
    - [Developer Token](#developer-token)
    - [OAuth 2.0 with Token Refresh](#oauth-20-with-token-refresh)
    - [JWT Authentication](#jwt-authentication)
    - [CCG Authentication](#ccg-authentication)
    - [Custom Network Configuration](#custom-network-configuration)
  - [Implementation Details](#implementation-details)
    - [Token Storage Adapter](#token-storage-adapter)
    - [Authentication Conversion](#authentication-conversion)
    - [Network Configuration Conversion](#network-configuration-conversion)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Overview

The configuration sharing feature allows developers to seamlessly migrate from the legacy SDK to the generated SDK by automatically extracting and converting authentication and network configuration from a legacy client to a generated client.

## Implementation Components

### Token Storage Adapter (`boxsdk/util/token_storage_adapter.py`)

The `LegacyTokenStorageAdapter` class bridges the gap between legacy OAuth2 token storage mechanisms (callbacks) and the generated SDK's `TokenStorage` interface.

**Key Features:**

- Converts legacy token format (access_token, refresh_token tuple) to generated SDK `AccessToken` objects
- Supports both read and write operations
- Handles token storage callbacks from legacy OAuth2 implementations

**Example:**

```python
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.util.token_storage_adapter import LegacyTokenStorageAdapter

from box_sdk_gen.box.oauth import BoxOAuth, OAuthConfig

# Legacy OAuth2 with a token persistence callback
stored_tokens = {"access": None, "refresh": None}


def store_tokens(access_token, refresh_token):
    stored_tokens["access"] = access_token
    stored_tokens["refresh"] = refresh_token


legacy_auth = OAuth2(client_id="...", client_secret="...", store_tokens=store_tokens)

# Bridge legacy token storage to the generated SDK TokenStorage interface
token_storage = LegacyTokenStorageAdapter(
    get_tokens=lambda: legacy_auth._get_tokens(),
    store_tokens=lambda access_token, refresh_token: legacy_auth._store_tokens(
        access_token, refresh_token
    ),
)

gen_auth = BoxOAuth(
    config=OAuthConfig(
        client_id="...",
        client_secret="...",
        token_storage=token_storage,
    )
)
```

### Client Methods

Three new methods have been added to the `Client` class in `boxsdk/client/client.py`:

#### `get_sdk_gen_client(auth_options=None, network_options=None)`

Creates a fully configured generated SDK client from the legacy client. This is the main convenience method that combines `get_sdk_gen_authentication()` and `get_sdk_gen_network_session()`.

**Parameters:**

- `auth_options` (optional): Dictionary with authentication options
  - `token_storage`: Custom `TokenStorage` instance
- `network_options` (optional): Dictionary with network options
  - `network_client`: Custom `NetworkClient` instance
  - `retry_strategy`: Custom `RetryStrategy` instance
  - `data_sanitizer`: Custom `DataSanitizer` instance
  - `additional_headers`: Dictionary of additional HTTP headers

**Returns:**

- `BoxClient` instance from `box_sdk_gen`, fully configured with shared settings

**Example:**

```python
from boxsdk import Client
from boxsdk.auth import OAuth2

# Legacy client setup
legacy_auth = OAuth2(client_id="...", client_secret="...")
legacy_client = Client(legacy_auth)

# Get generated SDK client with one line
gen_client = legacy_client.get_sdk_gen_client()

# Use generated client for new features
user = gen_client.users.get_user_by_id("me")
folders = gen_client.folders.get_folder_items("0")

# Legacy client still works for existing code
legacy_user = legacy_client.user().get()
```

#### `get_sdk_gen_authentication(token_storage=None)`

Extracts authentication configuration from the legacy client and converts it to a generated SDK `Authentication` object.

**Supported Authentication Types:**

- `DeveloperTokenAuth` → `BoxDeveloperTokenAuth`
- `OAuth2` → `BoxOAuth`
- `JWTAuth` → `BoxJWTAuth`
- `CCGAuth` → `BoxCCGAuth`

**Parameters:**

- `token_storage` (optional): Custom `TokenStorage` instance. If not provided, an adapter will be created to bridge legacy token storage.

**Returns:**

- `Authentication` object compatible with `box_sdk_gen`

**Example:**

```python
from boxsdk import Client
from boxsdk.auth import OAuth2
from box_sdk_gen.client import BoxClient

# Legacy client
legacy_auth = OAuth2(client_id="...", client_secret="...")
legacy_client = Client(legacy_auth)

# Get generated SDK authentication
gen_auth = legacy_client.get_sdk_gen_authentication()
gen_client = BoxClient(auth=gen_auth)
```

#### `get_sdk_gen_network_session(**options)`

Extracts network configuration from the legacy client and converts it to a generated SDK `NetworkSession` object.

**Parameters:**

- `network_client` (optional): Custom `NetworkClient` instance
- `retry_strategy` (optional): Custom `RetryStrategy` instance
- `data_sanitizer` (optional): Custom `DataSanitizer` instance
- `additional_headers` (optional): Dictionary of additional HTTP headers

**Returns:**

- `NetworkSession` object compatible with `box_sdk_gen`

**Configuration Mapping:**

- Base URLs: Extracted from `API` config
- Proxy settings: Extracted from `Proxy` config
- Retry strategy: Extracted from `API.MAX_RETRY_ATTEMPTS` and session retry settings
- Custom headers: Merged from session default headers and additional headers

**Example:**

```python
from boxsdk import Client
from box_sdk_gen.client import BoxClient
from box_sdk_gen.box.developer_token_auth import BoxDeveloperTokenAuth

legacy_client = Client(legacy_auth)

network_session = legacy_client.get_sdk_gen_network_session(
    additional_headers={"X-Custom-Header": "value"}
)

gen_auth = BoxDeveloperTokenAuth(token="...")
gen_client = BoxClient(auth=gen_auth, network_session=network_session)
```

## Usage Examples

### Developer Token

```python
from boxsdk import Client
from boxsdk.auth import DeveloperTokenAuth

legacy_auth = DeveloperTokenAuth()
legacy_client = Client(legacy_auth)

# Get generated client
gen_client = legacy_client.get_sdk_gen_client()
```

### OAuth 2.0 with Token Refresh

```python
from boxsdk import Client
from boxsdk.auth import OAuth2

legacy_auth = OAuth2(
    client_id="...", client_secret="...", access_token="...", refresh_token="..."
)
legacy_client = Client(legacy_auth)

# Get generated client with shared token storage
gen_client = legacy_client.get_sdk_gen_client()

# Both clients share the same token storage
# Token refresh by either updates both
```

### JWT Authentication

```python
from boxsdk import Client
from boxsdk.auth import JWTAuth

legacy_auth = JWTAuth(
    client_id="...",
    client_secret="...",
    enterprise_id="...",
    jwt_key_id="...",
    rsa_private_key_file_sys_path="path/to/key.pem",
)
legacy_client = Client(legacy_auth)

# Get generated client
gen_client = legacy_client.get_sdk_gen_client()

# Handle user vs enterprise scope
if user_id:
    gen_auth = legacy_client.get_authentication()
    gen_auth = gen_auth.with_user_subject(user_id)
    gen_client = BoxClient(
        auth=gen_auth, network_session=legacy_client.get_network_session()
    )
```

### CCG Authentication

```python
from boxsdk import Client
from boxsdk.auth import CCGAuth

legacy_auth = CCGAuth(client_id="...", client_secret="...", enterprise_id="...")
legacy_client = Client(legacy_auth)

# Get generated client
gen_client = legacy_client.get_sdk_gen_client()
```

### Custom Network Configuration

```python
from boxsdk import Client
from boxsdk.auth import OAuth2

legacy_client = Client(OAuth2(...))

# Get generated client with custom network options
gen_client = legacy_client.get_sdk_gen_client(
    network_options={
        "additional_headers": {"X-Custom-Header": "value"},
        "retry_strategy": custom_retry_strategy,
    }
)
```

## Implementation Details

### Token Storage Adapter

The `LegacyTokenStorageAdapter` implements the `TokenStorage` interface from `box_sdk_gen`:

- `store(token: AccessToken)`: Stores tokens using legacy storage mechanism
- `get() -> Optional[AccessToken]`: Retrieves tokens from legacy storage
- `clear()`: Clears stored tokens

The adapter converts between:

- Legacy format: `(access_token: str, refresh_token: Optional[str])`
- Generated format: `AccessToken(access_token, refresh_token, expires_in, token_type)`

### Authentication Conversion

Each authentication type is handled specifically:

1. **DeveloperTokenAuth**: Direct token extraction
2. **OAuth2**: Client ID/secret extraction + token storage adapter
3. **JWTAuth**: Full credential extraction including private key serialization
4. **CCGAuth**: Client ID/secret + enterprise/user ID extraction

### Network Configuration Conversion

Network settings are extracted from:

- `Session.api_config`: Base URLs, OAuth URLs
- `Session.proxy_config`: Proxy settings
- `Session._default_headers`: Custom headers
- `API.MAX_RETRY_ATTEMPTS`: Retry configuration
