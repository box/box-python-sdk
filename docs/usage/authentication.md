Authentication
==============

The Box API uses OAuth2 for authentication, which can be difficult to implement.
The SDK makes it easier by providing classes that handle obtaining tokens and
automatically refreshing them when possible. See the
[OAuth 2 overview](https://developer.box.com/en/guides/authentication/) for a detailed
overview of how the Box API handles authentication.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Ways to Authenticate](#ways-to-authenticate)
  - [Developer Token](#developer-token)
  - [Server Auth with JWT](#server-auth-with-jwt)
  - [Traditional 3-Legged OAuth2](#traditional-3-legged-oauth2)
    - [Redirect to Authorization URL](#redirect-to-authorization-url)
    - [Authenticate (Get Token Pair)](#authenticate-get-token-pair)
  - [Box View Authentication with App Tokens](#box-view-authentication-with-app-tokens)
- [As-User](#as-user)
- [Token Exchange](#token-exchange)
- [Revoking Tokens](#revoking-tokens)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Ways to Authenticate
--------------------

### Developer Token

The fastest way to get started using the API is with developer tokens. A
developer token is simply a short-lived access token that cannot be refreshed
and can only be used with your own account. Therefore, they're only useful for
testing an app and aren't suitable for production. You can obtain a developer
token from your application's [developer console][dev_console] page.

For manual testing in a Python REPL, you can interactively create a [`DevelopmentClient`][dev_client].
This client will prompt for a new developer token any time the current one expires, and will automatically
log API requests and responses for testing and debugging.

```python
>>> from boxsdk import DevelopmentClient
>>> client = DevelopmentClient()
Enter developer token: <ENTER DEVELOPER TOKEN HERE>
>>> me = client.user().get()
GET https://api.box.com/2.0/users/me {'headers': {'Authorization': '---wXyZ',
             'User-Agent': 'box-python-sdk-2.0.0',
             'X-Box-UA': 'agent=box-python-sdk/2.0.0; env=python/3.6.5'},
 'params': None}
"GET https://api.box.com/2.0/users/me" 200 454
{'Date': 'Tue, 30 Oct 2018 20:57:36 GMT', 'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Strict-Transport-Security': 'max-age=31536000', 'Cache-Control': 'no-cache, no-store', 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding', 'BOX-REQUEST-ID': '0dnjcjpu1krfunto6s7mrpal2ba', 'Age': '0'}
{'address': '',
 'avatar_url': 'https://cloud.app.box.com/api/avatar/large/33333',
 'created_at': '2012-06-07T11:14:50-07:00',
 'id': '33333',
 'job_title': '',
 'language': 'en',
 'login': 'user@example.com',
 'max_upload_size': 16106127360,
 'modified_at': '2018-10-29T12:13:57-07:00',
 'name': 'Example User',
 'phone': '',
 'space_amount': 1000000000000000.0,
 'space_used': 14330011102,
 'status': 'active',
 'timezone': 'America/Los_Angeles',
 'type': 'user'}
>>>
```

To create a [`Client`][client_class] non-interactively with a developer token, construct an [`OAuth2`][oauth2_class]
object with the `access_token` set to the developer token and construct the client with that.

<!-- sample x_auth init_with_dev_token -->
```python
from boxsdk import Client, OAuth2

auth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='DEVELOPER_TOKEN_GOES_HERE',
)
client = Client(auth)
me = client.user().get()
print(f'My user ID is {me.id}')
```

[dev_console]: https://app.box.com/developers/console
[dev_client]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#module-boxsdk.client.development_client
[client_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client
[oauth2_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.auth.html#boxsdk.auth.oauth2.OAuth2

### Server Auth with JWT

Authenticating with a JWT requires some extra dependencies. To get them, simply
```
pip install "boxsdk[jwt]"
```

Server auth allows your application to authenticate itself with the Box API
for a given enterprise.  By default, your application has a
[Service Account](https://developer.box.com/en/guides/authentication/user-types/app-users/)
that represents it and can perform API calls.  The Service Account is separate
from the Box accounts of the application developer and the enterprise admin of
any enterprise that has authorized the app — files stored in that account are
not accessible in any other account by default, and vice versa.

If you generated your public and private keys automatically through the
[Box Developer Console][dev_console], you can use the JSON file created there
to configure your SDK instance and create a client to make calls as the
Service Account by calling the appropriate static [`JWTAuth`][jwt_auth_class] method:

<!-- sample x_auth init_with_jwt_enterprise -->
```python
from boxsdk import JWTAuth, Client

auth = JWTAuth.from_settings_file('/path/to/settings.json')
client = Client(auth)
service_account = client.user().get()
print(f'Service Account user ID is {service_account.id}')
```

Otherwise, you'll need to provide the necessary configuration fields directly
to the [`JWTAuth`][jwt_auth_class] constructor:

<!-- sample x_auth init_with_jwt_enterprise_with_config -->
```python
from boxsdk import JWTAuth, Client

service_account_auth = JWTAuth(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    enterprise_id='YOUR_ENTERPRISE_ID',
    jwt_key_id='YOUR_JWT_KEY_ID',
    rsa_private_key_file_sys_path='CERT.PEM',
    rsa_private_key_passphrase='PASSPHRASE',
    store_tokens=your_store_tokens_callback_method,
)

access_token = auth.authenticate_instance()

service_account_client = Client(auth)
```

App auth applications also often have associated App Users, which are
[created and managed directly by the application](https://developer.box.com/en/guides/authentication/user-types/app-users/)
— they do not have normal login credentials, and can only be accessed through
the Box API by the application that created them.  You may authenticate as the
Service Account to provision and manage users, or as an individual app user to
make calls as that user.  See the [API documentation](https://developer.box.com/)
for detailed instructions on how to use app auth.

Clients for making calls as an App User can be created with the same [`JWTAuth`][jwt_auth_class]
constructor as in the above examples, similarly to creating a Service Account client.  Simply pass the
[`User`][user_class] object for the app user instead of an `enterprise_id` when constructing the auth instance:

<!-- sample x_auth init_with_jwt_with_user_id -->
```python
app_user = service_account_client.user(user_id='APP_USER_ID')

app_user_auth = JWTAuth(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user=app_user,
    jwt_key_id='YOUR_JWT_KEY_ID',
    rsa_private_key_file_sys_path='CERT.PEM',
    rsa_private_key_passphrase='PASSPHRASE',
    store_tokens=your_store_tokens_callback_method,
)
app_user_auth.authenticate_user()
app_user_client = Client(app_user_auth)
```

[jwt_auth_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.auth.html#boxsdk.auth.jwt_auth.JWTAuth
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User

### Traditional 3-Legged OAuth2

If your application needs to integrate with existing Box users who will provide
their login credentials to grant your application access to their account, you
will need to go through the standard OAuth2 login flow.  A detailed guide for
this process is available in the
[Authentication with OAuth API documentation](https://developer.box.com/en/guides/authentication/oauth2/).

Using an auth code is the most common way of authenticating with the Box API for
existing Box users, to integrate with their accounts.
Your application must provide a way for the user to login to Box (usually with a
browser or web view) in order to obtain an auth code.

After a user logs in and grants your application access to their Box account,
they will be redirected to your application's `redirect_uri` which will contain
an auth code. This auth code can then be used along with your client ID and
client secret to establish an API connection.

#### Redirect to Authorization URL

The first step in the process is to redirect the user to the Box Authorize URL, which you can generate
(along with a CSRF token) by calling [`oauth.get_authorization_url(redirect_url)`][get_authorization_url] with
your application's redirect URL.

<!-- sample get_authorize -->
```python
from boxsdk import OAuth2

oauth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    store_tokens=your_store_tokens_callback_method,
)

auth_url, csrf_token = oauth.get_authorization_url('http://YOUR_REDIRECT_URL')

# Redirect user to auth_url, where they will enter their Box credentials
```

The SDK will keep the tokens in memory for the duration of the Python script run, so you don't always need to pass
`store_tokens`.

[get_authorization_url]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.auth.html#boxsdk.auth.oauth2.OAuth2.get_authorization_url

#### Authenticate (Get Token Pair)

If you navigate the user to the auth_url, the user will be redirected to
`https://YOUR_REDIRECT_URL?code=YOUR_AUTH_CODE&state=CSRF_TOKEN` after they log in to Box.  After getting the auth code,
you will be able to exchange it for an access token and refresh token.

The SDK handles all the work for you; all you need to do is call [`oauth.authenticate(auth_code)`][authenticate] with
the auth code pulled from the query parameters of the incoming URL:

<!-- sample post_oauth2_token -->
```python
from boxsdk import Client

# Make sure that the csrf token you get from the `state` parameter
# in the final redirect URI is the same token you get from the
# get_authorization_url method to protect against CSRF vulnerabilities.
assert 'THE_CSRF_TOKEN_YOU_GOT' == csrf_token
access_token, refresh_token = oauth.authenticate('YOUR_AUTH_CODE')
client = Client(oauth)
```

[authenticate]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.auth.html#boxsdk.auth.oauth2.OAuth2.authenticate

#### Initialize a Client Given Access and Refresh Token

You can also instantiate a client given the access and refresh token. You first need to construct an
[OAuth2][oauth2_class] object with the access and refresh token passed in. Once you have created the
oauth object you then pass it into your [Client][client_class] object to instantiate your client. Finally, you can begin making calls with your client.

<!-- sample x_auth init_with_access_and_refresh_token -->
```python
from boxsdk import Client, OAuth2

oauth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='ACCESS_TOKEN',
    refresh_token='REFRESH_TOKEN',
)

client = Client(oauth)

user = client.user().get()
print(f'User ID is {user.id}')
```

### Box View Authentication with App Tokens

[Box View](https://developer.box.com/en/guides/embed/box-view/)
uses a long-lived access token that is generated from the [Box Developer Console][dev_console] to make API calls.
These access tokens cannot be automatically refreshed from the SDK, and must be manually changed in
your application code.

To use the primary or secondary access token generated in the Developer Console,
simply create a [`Client`][client_class] with that token:

<!-- sample x_auth init_with_app_token -->
```python
from boxsdk import Client, OAuth2

auth = OAuth2(
  client_id='YOUR_CLIENT_ID', 
  client_secret='', 
  access_token='APP_ACCESS_TOKEN_GOES_HERE'
)
client = Client(auth)
```

As-User
-------

The As-User header is used by enterprise admins to make API calls on behalf of
their enterprise's users. This requires the API request to pass an
`As-User: USER-ID` header. For more details see the
[documentation on As-User](https://developer.box.com/en/guides/authentication/oauth2/as-user/).

The following examples assume that the `client` has been instantiated with an
access token belonging to an admin-level user or Service Account with appropriate
privileges to make As-User calls.

Calling the [`client.as_user(user)`][as_user] method with the [`User`][user_class] creates a new client to impersonate
the provided user.  All calls made with the new client will be made in context of the impersonated user, leaving the
original client unmodified.

<!-- sample x_auth init_with_as_user_header -->
```python
user_to_impersonate = client.user(user_id='USER_ID_GOES_HERE')
user_client = client.as_user(user_to_impersonate)
```

[as_user]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.cloneable.Cloneable.as_user

Token Exchange
--------------

You can exchange a client's access token for one with a lower scope, in order
to restrict the permissions for a child client or to pass to a less secure
location (e.g. a browser-based app).  This is useful if you want to use the
[Box UI Elements](https://developer.box.com/en/guides/embed/ui-elements/), since they generally
do not need full read/write permissions to run.

To exchange the token held by a client for a new token with only `item_preview`
scope, restricted to a single file, suitable for the
[Content Preview UI Element](https://developer.box.com/en/guides/embed/ui-elements/preview/), call
[`client.downscope_token(scopes, item=None, additional_data=None)`][downscope_token] with the scope(s) needed.
This method returns a [`TokenResponse`][token_response] object with the downscoped token information.

<!-- sample post_oauth2_token downscope_token -->
```python
target_file = client.file(file_id='FILE_ID_HERE')
token_info = client.downscope_token(['item_preview'], target_file)
print(f'Got downscoped access token: {token_info.access_token}')
```

[downscope_token]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.downscope_token
[token_response]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.auth.html#boxsdk.auth.oauth2.TokenResponse

Revoking Tokens
---------------

To revoke the tokens contained in an [`OAuth2`][oauth2_class] instance, removing the ability to call the Box API,
call [`oauth.revoke()`][revoke].

<!-- sample post_oauth2_revoke -->
```python
oauth.revoke()
```

[revoke]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.auth.html#boxsdk.auth.oauth2.OAuth2.revoke
