# Migration guide from `boxsdk` to `box-sdk-gen`

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Installation](#installation)
- [Key differences](#key-differences)
  - [Manager approach](#manager-approach)
  - [Explicitly defined schemas](#explicitly-defined-schemas)
  - [Immutable design](#immutable-design)
- [Authentication](#authentication)
  - [Developer Token](#developer-token)
  - [JWT Auth](#jwt-auth)
    - [Using JWT configuration file](#using-jwt-configuration-file)
    - [Providing JWT configuration manually](#providing-jwt-configuration-manually)
    - [Authenticate user](#authenticate-user)
  - [Client Credentials Grant](#client-credentials-grant)
    - [Obtaining Service Account token](#obtaining-service-account-token)
    - [Obtaining User token](#obtaining-user-token)
  - [Switching between Service Account and User](#switching-between-service-account-and-user)
  - [OAuth 2.0 Auth](#oauth-20-auth)
    - [Get Authorization URL](#get-authorization-url)
    - [Authenticate](#authenticate)
  - [Store token and retrieve token callbacks](#store-token-and-retrieve-token-callbacks)
  - [Downscope token](#downscope-token)
  - [Revoke token](#revoke-token)
- [Configuration](#configuration)
  - [As-User header](#as-user-header)
  - [Custom Base URLs](#custom-base-urls)
- [Convenience methods](#convenience-methods)
  - [Webhook validation](#webhook-validation)
  - [Chunked upload of big files](#chunked-upload-of-big-files)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

The new `box-sdk-gen` SDK library, which helps Python developers to conveniently integrate with Box API.
In the contrary to the previous library (`boxsdk`), it is not manually maintained, but auto-generated
based on Open API Specification. This means you can leverage the most up-to-date Box API features in your
applications without delay. More information and benefits of using the new can be found in the
[README](https://github.com/box/box-python-sdk-gen/blob/main/README.md) file.

## Installation

To install a new Box Python SDK GENERATED use command:

```console
pip install box-sdk-gen
```

The new Box Python SDK GENERATED library could be used in the same project along with the legacy one.
If you want to use a feature available only in the new SDK, you don't need to necessarily migrate all your code
to use Box Python SDK GENERATED at once. You can use a new feature from the new library,
while keeping the rest of your code unchanged. Note that it may be required to alias some imported names
from the new SDK to avoid conflicts with the old one. However, we recommend to fully migrate to the new SDK eventually.

## Key differences

### Manager approach

The main difference between the old SDK and the new one is the way how API methods are aggregated into objects.

**Old (`boxsdk`)**

Firstly, in the old SDK to be able to perform any action on an API object, e.g. `User`, you first had to create its class.
To do it is required to call:

```python
user = client.user(user_id='123456')
```

to create a class representing an already existing User with id '12345', or create a new one with a call:

```python
user = client.create_user(name='Some User')
```

Then, you could perform any action on created class, which will affect the user, e.g.

```python
updated_user = user.update_info(data={'name': 'New User Name'})
```

**New (`box-sdk-gen`)**

In the new SDK the API methods are grouped into dedicated manager classes, e.g. `User` object
has dedicated `UserManager` class. Each manager class instance is available in `BoxClient` object.
The fields storing references to the managers are named in the plural form of the resource that the
manager handles - `client.users` for `UsersManager`. If you want to perform any operation
connected with a `User` you need to call a respective method of `UserManager`.
For example, to get info about existing user you need to call:

```python
user = client.users.get_user_by_id(user_id='123456')
```

or to create a new user:

```python
user = client.users.create_user(name='Some User')
```

The `User` object returned by both of these methods is a data class - it does not contain any methods to call.
To perform any action on `User` object, you need to still use a `UserManager` method for that.
Usually these methods have a first argument, which accepts id of the object you want to access,
e.g. to update a user name, call method:

```python
updated_user = client.users.update_user_by_id(user_id=user.id, name='New User Name')
```

### Explicitly defined schemas

**Old (`boxsdk`)**

In the old SDK there were no data types explicitly defined -
the responses were dynamically mapped into classes in the runtime. For example, if you get information about a file:

```python
file = client.file(file_id='12345678').get()
```

you couldn't be sure which fields to expect in the response object until the runtime,
because `File` class doesn't have any predefined fields.

**New (`box-sdk-gen`)**

In the new SDK the data classe are defined in `schemas` module, so you know, which fields to expect before
actually making a call. For example `FileBase` class is defined this way:

```python
class FileBase(BaseObject):
    def __init__(self, id: str, *, etag: Optional[str] = None, type: FileBaseTypeField = FileBaseTypeField.FILE.value, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.etag = etag
```

### Immutable design

The new SDK is designed to be mostly immutable. This means that methods,
which used to modify the existing object in old SDK now return a new instance of the class with the modified state.
This design pattern is used to avoid side effects and make the code more predictable and easier to reason about.
Methods, which returns a new modified instance of an object, will always have a prefix `with_` in their names, e.g.

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxClient

as_user_client: BoxClient = client.with_as_user_header('USER_ID')
```

## Authentication

The Box Python SDK GENERATED library offers the same authentication methods as the legacy one.
Let's see the differences of their usage:

### Developer Token

**Old (`boxsdk`)**

```python
from boxsdk import Client, OAuth2

auth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='DEVELOPER_TOKEN_GOES_HERE',
)
client = Client(auth)
```

The new SDK provides a convenient `BoxDeveloperTokenAuth`, which allows authenticating
using developer token without necessity to provide a Client ID and Client Secret

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

auth = BoxDeveloperTokenAuth(token='DEVELOPER_TOKEN_GOES_HERE')
client = BoxClient(auth=auth)
```

### JWT Auth

#### Using JWT configuration file

**Old (`boxsdk`)**

The static method, which reads the JWT configuration file has been changed:

```python
from boxsdk import JWTAuth, Client

auth = JWTAuth.from_settings_file('/path/to/config.json')
client = Client(auth)
```

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxClient, BoxJWTAuth, JWTConfig

jwt_config = JWTConfig.from_config_file(config_file_path='/path/to/config.json')
auth = BoxJWTAuth(config=jwt_config)
client = BoxClient(auth=auth)
```

#### Providing JWT configuration manually

Some params in `JWTConfig` constructor have slightly different names than one in old `JWTAuth` class.

**Old (`boxsdk`)**

```python
from boxsdk import JWTAuth

auth = JWTAuth(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    enterprise_id='YOUR_ENTERPRISE_ID',
    user_id='USER_ID',
    jwt_key_id='YOUR_JWT_KEY_ID',
    rsa_private_key_file_sys_path='CERT.PEM',
    rsa_private_key_passphrase='PASSPHRASE',
    jwt_algorithm='RS256',
)
```

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxJWTAuth, JWTConfig, JwtAlgorithm

jwt_config = JWTConfig(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    enterprise_id='YOUR_ENTERPRISE_ID',
    user_id='USER_ID',
    jwt_key_id='YOUR_JWT_KEY_ID',
    private_key='YOUR_PRIVATE_KEY',
    private_key_passphrase='PASSPHRASE',
    algorithm=JwtAlgorithm.RS256,
)
auth = BoxJWTAuth(config=jwt_config)
```

#### Authenticate user

In old SDK method for user authentication was named `authenticate_user(self, user: Union[str, 'User'] = None) -> str`
and was accepting either user object or user id. If none provided, user ID stored in `JWTAuth` class instance was used.
The `authenticate_user` method was modifying existing `BoxJWTAuth` class, which was exchanging the existing token with
the one with the user access.

**Old (`boxsdk`)**

```python
auth.authenticate_user(user)
```

or

```python
auth.authenticate_user('USER_ID')
```

**New (`box-sdk-gen`)**

In new SDK, to authenticate as user you need to call
`with_user_subject(self, user_id: str, *, token_storage: TokenStorage = None) -> BoxJWTAuth` method with id of the user
to authenticate. The method returns a new instance of `BoxJWTAuth` class, which will perform authentication call
in scope of the user on the first API call. The `token_storage` parameter is optional and allows to provide a custom
token storage for the new instance of `BoxJWTAuth` class. The new auth instance can be used to create a new user client
instance.

```python
from box_sdk_gen import BoxJWTAuth, BoxClient
user_auth: BoxJWTAuth = auth.with_user_subject('USER_ID')
user_client: BoxClient = BoxClient(auth=user_auth)
```

### Client Credentials Grant

#### Obtaining Service Account token

To authenticate as enterprise, the only difference between the old and the new SDK,
is using the `CCGConfig` as a middle step.

**Old (`boxsdk`)**

```python
from boxsdk import CCGAuth, Client

auth = CCGAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    enterprise_id="YOUR_ENTERPRISE_ID",
)

client = Client(auth)
```

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxClient, BoxCCGAuth, CCGConfig

ccg_config = CCGConfig(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    enterprise_id="YOUR_ENTERPRISE_ID",
)
auth = BoxCCGAuth(config=ccg_config)
client = BoxClient(auth=auth)
```

#### Obtaining User token

In old SDK `CCGAuth` was accepting both user object and User ID. In the box-sdk-gen the `BoxCCGAuth` constructor accepts
only User ID instead.

**Old (`boxsdk`)**

```python
from boxsdk import CCGAuth

auth = CCGAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user="YOUR_USER_ID"
)
```

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxCCGAuth, CCGConfig

ccg_config = CCGConfig(
  client_id="YOUR_CLIENT_ID",
  client_secret="YOUR_CLIENT_SECRET",
  user_id="YOUR_USER_ID"
)
auth = BoxCCGAuth(config=ccg_config)
```

### Switching between Service Account and User

In old SDK there were two methods which allowed to switch between using service and user account. Calling these methods
were modifying existing state of `CCGAuth` class, which was fetching a new token on the next API call.

**Old (`boxsdk`)**

```python
auth.authenticate_enterprise('ENTERPRISE_ID')
```

```python
auth.authenticate_user('USER_ID')
```

In the new SDK, to keep the immutability design, the methods switching authenticated subject were replaced with methods
returning a new instance of `BoxCCGAuth` class. The new instance will fetch a new token on the next API call.
The new auth instance can be used to create a new client instance. You can also specify `token_storage` parameter
to provide a custom token storage for the new instance.
The old instance of `BoxCCGAuth` class will remain unchanged and will still use the old token.

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxCCGAuth, BoxClient
enterprise_auth: BoxCCGAuth = auth.with_enterprise_subject(enterprise_id='ENTERPRISE_ID')
enterprise_client: BoxClient = BoxClient(auth=enterprise_auth)
```

```python
from box_sdk_gen import BoxCCGAuth, BoxClient
user_auth: BoxCCGAuth = auth.with_user_subject(user_id='USER_ID')
user_client: BoxClient = BoxClient(auth=user_auth)
```

Note that the new methods accept only user id or enterprise id, while the old ones were accepting
user and enterprise object too.

### OAuth 2.0 Auth

#### Get Authorization URL

To get authorization url in the new SDK, you need to first create the `BoxOAuth` class (previously `OAuth2`) using
`OAuthConfig` class. Then to get authorization url, call
`get_authorize_url(self, *, options: GetAuthorizeUrlOptions = None) -> str` instead of
`get_authorization_url(self, redirect_url: Optional[str]) -> Tuple[str, str]`. Note that this method
now accepts the instance of `GetAuthorizeUrlOptions` class, which allows specifying extra options to API call.
The new function returns only the authentication url string, while the old one returns tuple of
authentication url and csrf_token.

**Old (`boxsdk`)**

```python
from boxsdk import OAuth2

auth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
)

auth_url, csrf_token = auth.get_authorization_url('http://YOUR_REDIRECT_URL')
```

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxOAuth, OAuthConfig, GetAuthorizeUrlOptions

auth = BoxOAuth(
  OAuthConfig(
      client_id='YOUR_CLIENT_ID',
      client_secret='YOUR_CLIENT_SECRET',
  )
)
auth_url = auth.get_authorize_url(options=GetAuthorizeUrlOptions(redirect_uri='http://YOUR_REDIRECT_URL'))
```

#### Authenticate

The signature of method for authenticating with obtained auth code got changed from:
`authenticate(self, auth_code: Optional[str]) -> Tuple[str, str]` to
`get_tokens_authorization_code_grant(self, authorization_code: str, *, network_session: Optional[NetworkSession] = None) -> AccessToken`.
The method now returns an AccessToken object with `access_token` and `refresh_token` fields,
while the old one was returning a tuple of access token and refresh token.

**Old (`boxsdk`)**

```python
from boxsdk import Client
access_token, refresh_token = auth.authenticate('YOUR_AUTH_CODE')
client = Client(auth)
```

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxClient, AccessToken

access_token: AccessToken = auth.get_tokens_authorization_code_grant('YOUR_AUTH_CODE')
client = BoxClient(auth)
```

### Store token and retrieve token callbacks

In old SDK you could provide a `store_tokens` callback method to an authentication class, which was called each time
an access token was refreshed. It could be used to save your access token to a custom token storage
and allow to reuse this token later.
What is more, old SDK allowed also to provide `retrieve_tokens` callback, which is called each time the SDK needs to use
token to perform an API call. To provide that, it was required to use `CooperativelyManagedOAuth2` and provide
`retrieve_tokens` callback method to its constructor.

**Old (`boxsdk`)**

```python
from typing import Tuple
from boxsdk.auth import CooperativelyManagedOAuth2
from boxsdk import Client

def retrieve_tokens() -> Tuple[str, str]:
    # retrieve access_token and refresh_token
    return access_token, refresh_token

def store_tokens(access_token: str, refresh_token: str):
    # store access_token and refresh_token
    pass


auth = CooperativelyManagedOAuth2(
  client_id='YOUR_CLIENT_ID',
  client_secret='YOUR_CLIENT_SECRET',
  retrieve_tokens=retrieve_tokens,
  store_tokens=store_tokens
)
access_token, refresh_token = auth.authenticate('YOUR_AUTH_CODE')
client = Client(auth)
```

In the new SDK you can define your own class delegated for storing and retrieving a token. It has to inherit from
`TokenStorage` and implement all of its abstract methods. Next step would be to pass an instance of this class to the
AuthConfig constructor.

**New (`box-sdk-gen`)**

```python
from typing import Optional
from box_sdk_gen import BoxOAuth, OAuthConfig, TokenStorage, AccessToken

class MyCustomTokenStorage(TokenStorage):
  def store(self, token: AccessToken) -> None:
    # store token
    pass

  def get(self) -> Optional[AccessToken]:
    # get token
    pass

  def clear(self) -> None:
    # clear token
    pass


auth = BoxOAuth(
  OAuthConfig(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    token_storage=MyCustomTokenStorage()
  )
)
```

or reuse one of the provided implementations: `FileTokenStorage` or `FileWithInMemoryCacheTokenStorage`:

```python
from box_sdk_gen import BoxOAuth, OAuthConfig, FileWithInMemoryCacheTokenStorage

auth = BoxOAuth(
  OAuthConfig(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    token_storage=FileWithInMemoryCacheTokenStorage()
  )
)
```

### Downscope token

The process of downscoping token in the new SDK is similar to the old one. The main difference is that the new method
accepts the full resource path instead of file object.

**Old (`boxsdk`)**

```python
from boxsdk import Client, OAuth2

target_file = client.file(file_id='FILE_ID_HERE')
token_info = client.downscope_token(['item_preview'], target_file)
downscoped_auth = OAuth2(
  client_id=None,
  client_secret=None,
  access_token=token_info.access_token
)
downscoped_client = Client(downscoped_auth)
```

**New (`box-sdk-gen`)**

```python
from box_sdk_gen import BoxDeveloperTokenAuth, AccessToken, BoxClient

resource = 'https://api.box.com/2.0/files/123456789'
downscoped_token: AccessToken = auth.downscope_token(
    scopes=['item_preview'],
    resource=resource,
)
downscoped_auth = BoxDeveloperTokenAuth(token=downscoped_token.access_token)
client = BoxClient(auth=downscoped_auth)
```

### Revoke token

To revoke current client's tokens in the new SDK, you need to call `revoke_token` method of the auth class instead of
`revoke` method.

**Old (`boxsdk`)**

```python
oauth.revoke()
```

**New (`box-sdk-gen`)**

```python
client.auth.revoke_token()
```

## Configuration

### As-User header

The As-User header is used by enterprise admins to make API calls on behalf of their enterprise's users.
This requires the API request to pass an `As-User: USER-ID` header. The following examples assume that the client has
been instantiated with an access token with appropriate privileges to make As-User calls.

In old SDK you could call client `as_user(self, user: User)` method to create a new client to impersonate the provided user.

**Old (`boxsdk`)**

```python
from boxsdk import Client

user_to_impersonate = client.user(user_id='USER_ID')
user_client: Client = client.as_user(user_to_impersonate)
```

**New (`box-sdk-gen`)**

In the new SDK the method was renamed to `with_as_user_header(self, user_id: str) -> BoxClient`
and returns a new instance of `BoxClient` class with the As-User header appended to all API calls made by the client.
The method accepts only user id as a parameter.

```python
from box_sdk_gen import BoxClient

user_client: BoxClient = client.with_as_user_header(user_id='USER_ID')
```

Additionally `BoxClient` offers a `with_extra_headers(self, *, extra_headers: Dict[str, str] = None) -> BoxClient`
method, which allows you to specify the custom set of headers, which will be included in every API call made by client.
Calling the `client.with_extra_headers()` method creates a new client, leaving the original client unmodified.

```python
from box_sdk_gen import BoxClient

new_client: BoxClient = client.with_extra_headers(extra_headers={'customHeader': 'customValue'})
```

### Custom Base URLs

**Old (`boxsdk`)**

In old SDK you could specify the custom base URLs, which will be used for API calls made by setting
the new values of static variables of the `API` class.

```python
from boxsdk.config import API

API.BASE_API_URL = 'https://new-base-url.com'
API.OAUTH2_API_URL = 'https://my-company.com/oauth2'
API.UPLOAD_URL = 'https://my-company-upload-url.com'
```

**New (`box-sdk-gen`)**

In the new SDK this functionality has been implemented as part of the `BoxClient` class.
By calling the `client.with_custom_base_urls()` method, you can specify the custom base URLs that will be used for API
calls made by client. Following the immutability pattern, this call creates a new client, leaving the original client unmodified.

```python
from box_sdk_gen import BoxClient, BaseUrls

new_client: BoxClient = client.with_custom_base_urls(base_urls=BaseUrls(
  base_url='https://new-base-url.com',
  upload_url='https://my-company-upload-url.com',
  oauth_2_url='https://my-company.com/oauth2',
))
```

## Convenience methods

### Webhook validation

Webhook validation is used to validate a webhook message by verifying the signature and the delivery timestamp.

**Old (`boxsdk`)**

In the old SDK, you could pass the `body` as `bytes`, and it would return a `boolean` value indicating whether the message was valid.

```python
body = b'{"webhook":{"id":"1234567890"},"trigger":"FILE.UPLOADED","source":{"id":"1234567890","type":"file","name":"Test.txt"}}'
headers = {
    'box-delivery-id': 'f96bb54b-ee16-4fc5-aa65-8c2d9e5b546f',
    'box-delivery-timestamp': '2020-01-01T00:00:00-07:00',
    'box-signature-algorithm': 'HmacSHA256',
    'box-signature-primary': '4KvFa5/unRL8aaqOlnbInTwkOmieZkn1ZVzsAJuRipE=',
    'box-signature-secondary': 'yxxwBNk7tFyQSy95/VNKAf1o+j8WMPJuo/KcFc7OS0Q=',
    'box-signature-version': '1',
}
is_validated = Webhook.validate_message(body, headers, primary_key, secondary_key)
print(f'The webhook message is validated to: {is_validated}')
```

**New (`box-sdk-gen`)**

In the new SDK, the `WebhooksManager.validate_message()` method requires the `body` to be of type `string` and
the rest of the code remains the same

```python
from box_sdk_gen import WebhooksManager

body = '{"webhook":{"id":"1234567890"},"trigger":"FILE.UPLOADED","source":{"id":"1234567890","type":"file","name":"Test.txt"}}'
headers = {
  'box-delivery-id': 'f96bb54b-ee16-4fc5-aa65-8c2d9e5b546f',
  'box-delivery-timestamp': '2020-01-01T00:00:00-07:00',
  'box-signature-algorithm': 'HmacSHA256',
  'box-signature-primary': '4KvFa5/unRL8aaqOlnbInTwkOmieZkn1ZVzsAJuRipE=',
  'box-signature-secondary': 'yxxwBNk7tFyQSy95/VNKAf1o+j8WMPJuo/KcFc7OS0Q=',
  'box-signature-version': '1',
}
WebhooksManager.validate_message(
        body=body, headers=headers, primary_key=primary_key, secondary_key=secondary_key
)
```

### Chunked upload of big files

For large files or in cases where the network connection is less reliable, you may want to upload the file in parts.
This allows a single part to fail without aborting the entire upload, and failed parts are being retried automatically.

**Old (`boxsdk`)**

In the old SDK, you could use the `get_chunked_uploader()` method to create a chunked uploader object.
Then, you would call the `start()` method to begin the upload process.
The `get_chunked_uploader()` method requires the `file_path` and `file_name` parameters.

```python
chunked_uploader = client.folder('0').get_chunked_uploader(file_path='/path/to/file.txt', file_name='new_name.txt')
uploaded_file = chunked_uploader.start()
print(f'File "{uploaded_file.name}" uploaded to Box with file ID {uploaded_file.id}')
```

**New (`box-sdk-gen`)**

In the new SDK, the equivalent method is `chunked_uploads.upload_big_file()`. It accepts a file-like object
as the `file` parameter, and the `file_name` and `file_size` parameters are now passed as arguments.
The `parent_folder_id` parameter is also required to specify the folder where the file will be uploaded.

```python
import os

with open('/path/to/file.txt', 'rb') as file_byte_stream:
    file_name = 'new_name.txt'
    file_size = os.path.getsize('/path/to/file.txt')
    parent_folder_id = '0'  # ID of the folder where the file will be uploaded
    uploaded_file = client.chunked_uploads.upload_big_file(
        file=file_byte_stream, file_name=file_name, file_size=file_size, parent_folder_id=parent_folder_id
    )
```
