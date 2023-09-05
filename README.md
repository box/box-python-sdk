<p align="center">
  <img src="https://github.com/box/sdks/blob/master/images/box-dev-logo.png" alt= “box-dev-logo” width="30%" height="50%">
</p>

# Box Python SDK

[![image](http://opensource.box.com/badges/active.svg)](http://opensource.box.com/badges)
[![Documentation Status](https://readthedocs.org/projects/box-python-sdk/badge/?version=latest)](http://box-python-sdk.readthedocs.org/en/latest)
[![image](https://github.com/box/box-python-sdk/workflows/build/badge.svg)](https://github.com/box/box-python-sdk/actions)
[![image](https://img.shields.io/pypi/v/boxsdk.svg)](https://pypi.python.org/pypi/boxsdk)
[![image](https://img.shields.io/pypi/dm/boxsdk.svg)](https://pypi.python.org/pypi/boxsdk)
[![image](https://coveralls.io/repos/github/box/box-python-sdk/badge.svg?branch=main)](https://coveralls.io/github/box/box-python-sdk?branch=main)

Getting Started Docs: <https://developer.box.com/guides/tooling/sdks/python/>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installing](#installing)
- [Getting Started](#getting-started)
- [Authorization](#authorization)
  - [Server-to-Server Auth with JWT](#server-to-server-auth-with-jwt)
  - [Traditional 3-legged OAuth2](#traditional-3-legged-oauth2)
  - [Other Auth Options](#other-auth-options)
- [Usage Documentation](#usage-documentation)
  - [Making API Calls Manually](#making-api-calls-manually)
- [Other Client Options](#other-client-options)
  - [Logging Client](#logging-client)
  - [Developer Token Client](#developer-token-client)
  - [Development Client](#development-client)
- [Customization](#customization)
  - [Custom Subclasses](#custom-subclasses)
- [FIPS 140-2 Compliance](#fips-140-2-compliance)
- [Versions](#versions)
  - [Supported Version](#supported-version)
  - [Version schedule](#version-schedule)
- [Contributing](#contributing)
  - [Developer Setup](#developer-setup)
  - [Testing](#testing)
- [Questions, Bugs, and Feature Requests?](#questions-bugs-and-feature-requests)
- [Copyright and License](#copyright-and-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Installing

``` console
pip install boxsdk
```

The current version of the SDK is v3.x --- With this release support for
Python 3.5 and earlier (including 2.x) has been dropped. if you're
looking for the code or documentation for v1.5.x, please see the [1.5
branch](https://github.com/box/box-python-sdk/tree/1.5).

# Getting Started

To get started with the SDK, get a Developer Token from the
Configuration page of your app in the [Box Developer
Console](https://app.box.com/developers/console). You can use this token
to make test calls for your own Box account.

The SDK provides an interactive `DevelopmentClient` that makes it easy
to test out the SDK in a REPL. This client will automatically prompt for
a new Developer Token when it requires one, and will log HTTP requests
and responses to aid in debugging and understanding how the SDK makes
API calls.

``` pycon
>>> from boxsdk import DevelopmentClient
>>> client = DevelopmentClient()
Enter developer token: <ENTER DEVELOPER TOKEN HERE>
>>> user = client.user().get()
GET https://api.box.com/2.0/users/me {'headers': {'Authorization': '---wXyZ',
            'User-Agent': 'box-python-sdk-2.0.0',
            'X-Box-UA': 'agent=box-python-sdk/2.0.0; env=python/3.6.5'},
'params': None}
"GET https://api.box.com/2.0/users/me" 200 454
{'Date': 'Thu, 01 Nov 2018 23:32:11 GMT', 'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Strict-Transport-Security': 'max-age=31536000', 'Cache-Control': 'no-cache, no-store', 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding', 'BOX-REQUEST-ID': '0b50luc09ahp56m2jmkla8mgmh2', 'Age': '0'}
{'address': '',
'avatar_url': 'https://cloud.app.box.com/api/avatar/large/123456789',
'created_at': '2012-06-07T11:14:50-07:00',
'id': '123456789',
'job_title': '',
'language': 'en',
'login': 'user@example.com',
'max_upload_size': 16106127360,
'modified_at': '2018-10-30T17:01:27-07:00',
'name': 'Example User',
'phone': '',
'space_amount': 1000000000000000.0,
'space_used': 14330018065,
'status': 'active',
'timezone': 'America/Los_Angeles',
'type': 'user'}

>>> print(f'The current user ID is {user.id}')
The current user ID is 123456789
```

Outside of a REPL, you can initialize a new `Client` with just the
Developer Token to get started.

``` python
from boxsdk import OAuth2, Client

auth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='YOUR_DEVELOPER_TOKEN',
)
client = Client(auth)

user = client.user().get()
print(f'The current user ID is {user.id}')
```

# Authorization

The Box API uses OAuth2 for auth. The SDK makes it relatively painless
to work with OAuth2 tokens.

## Server-to-Server Auth with JWT

The Python SDK supports your [JWT
Authentication](https://developer.box.com/en/guides/authentication/jwt/)
applications.

Authenticating with a JWT requires some extra dependencies. To get them,
simply

``` console
pip install "boxsdk[jwt]"
```

Instead of instantiating your `Client` with an instance of `OAuth2`,
instead use an instance of `JWTAuth`.

``` python
from boxsdk import JWTAuth
from boxsdk import Client

auth = JWTAuth(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    enterprise_id='YOUR_ENTERPRISE_ID',
    jwt_key_id='YOUR_JWT_KEY_ID',
    rsa_private_key_file_sys_path='CERT.PEM',
    rsa_private_key_passphrase='PASSPHRASE',
)

access_token = auth.authenticate_instance()
client = Client(auth)
```

This client is able to create application users:

``` python
ned_stark_user = client.create_user('Ned Stark')
```

These users can then be authenticated:

``` python
ned_auth = JWTAuth(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user=ned_stark_user,
    jwt_key_id='YOUR_JWT_KEY_ID',
    rsa_private_key_file_sys_path='CERT.PEM',
    rsa_private_key_passphrase='PASSPHRASE'
)
ned_auth.authenticate_user()
ned_client = Client(ned_auth)
```

Requests made with `ned_client` (or objects returned from
`ned_client`'s methods) will be performed on behalf of the newly
created app user.

## Traditional 3-legged OAuth2

### Get the Authorization URL

``` python
from boxsdk import OAuth2

oauth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    store_tokens=your_store_tokens_callback_method,
)

auth_url, csrf_token = oauth.get_authorization_url('http://YOUR_REDIRECT_URL')
```

store_tokens is a callback used to store the access token and refresh
token. You might want to define something like this:

``` python
def store_tokens(access_token, refresh_token):
    # store the tokens at secure storage (e.g. Keychain)
```

The SDK will keep the tokens in memory for the duration of the Python
script run, so you don't always need to pass store_tokens.

### Authenticate (Get Access/Refresh Tokens)

If you navigate the user to the auth_url, the user will eventually get
redirected to <http://YOUR_REDIRECT_URL?code=YOUR_AUTH_CODE>. After
getting the code, you will be able to use the code to exchange for an
access token and refresh token.

The SDK handles all the work for you; all you need to do is run:

``` python
# Make sure that the csrf token you get from the `state` parameter
# in the final redirect URI is the same token you get from the
# get_authorization_url method.
assert 'THE_CSRF_TOKEN_YOU_GOT' == csrf_token
access_token, refresh_token = oauth.authenticate('YOUR_AUTH_CODE')
```

### Create an Authenticated Client

``` python
from boxsdk import Client

client = Client(oauth)
```

And that's it! You can start using the client to do all kinds of cool
stuff and the SDK will handle the token refresh for you automatically.

### Instantiate a Client Given an Access and a Refresh Token

Alternatively, you can instantiate an OAuth2 object with the access
token and refresh token. Once you have an oauth object you can pass that
into the Client object to instantiate a client and begin making calls.

``` python
from boxsdk import Client, OAuth2

oauth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='ACCESS_TOKEN',
    refresh_token='REFRESH_TOKEN',
)

client = Client(oauth)
user = client.user().get()
```

This will retrieve the current user! From here you can use the client
you created to start making calls.

## Other Auth Options

For advanced uses of the SDK, three additional auth classes are
provided:

-   `CooperativelyManagedOAuth2`: Allows multiple auth instances to
    share tokens.
-   `RemoteOAuth2`: Allows use of the SDK on clients without access to
    your application's client secret. Instead, you provide a
    `retrieve_access_token` callback. That callback should perform the
    token refresh, perhaps on your server that does have access to the
    client secret.
-   `RedisManagedOAuth2`: Stores access and refresh tokens in Redis.
    This allows multiple processes (possibly spanning multiple machines)
    to share access tokens while synchronizing token refresh. This could
    be useful for a multiprocess web server, for example.

# Usage Documentation

Full documentation of the available functionality with example code is
available in the [SDK documentation
pages](https://github.com/box/box-python-sdk/blob/main/docs/usage), and
there is also method-level documentation available on
[ReadTheDocs](https://box-python-sdk.readthedocs.io/en/stable/index.html).

## Making API Calls Manually

The Box API is continually evolving. As such, there are API endpoints
available that are not specifically supported by the SDK. You can still
use these endpoints by using the `make_request` method of the `Client`.

``` python
# https://developer.box.com/en/reference/get-metadata-templates-id/
# Returns a Python dictionary containing the result of the API request
json_response = client.make_request(
    'GET',
    client.get_url('metadata_templates', 'enterprise', 'customer', 'schema'),
).json()
```

`make_request()` takes two parameters:

-   `method` - an HTTP verb like `GET` or `POST`
-   `url` - the URL of the requested API endpoint

The `Client` class and Box objects have a `get_url` method. Pass it an
endpoint to get the correct URL for use with that object and endpoint.

For API calls which require body or query params, you can use `**kwargs`
to pass extra params:

-   `data` - takes a jsonified dictionary of body parameters
-   `params` - takes a dictionary of query parameters

``` python
# https://developer.box.com/reference/post-folders/
# Creates a new folder

# JSONify the body
body = json.dumps({
        'name': 'test-subfolder',
        'parent': {
            'id': '0',
        }
})

client.make_request(
    'POST',
    client.get_url('folders'),
    params={'fields': 'name,id'},
    data=body
)
```

# Other Client Options

## Logging Client

For more insight into the network calls the SDK is making, you can use
the `LoggingClient` class. This class logs information about network
requests and responses made to the Box API.

``` pycon
>>> from boxsdk import LoggingClient
>>> client = LoggingClient()
>>> client.user().get()
GET https://api.box.com/2.0/users/me {'headers': {u'Authorization': u'Bearer ---------------------------kBjp',
             u'User-Agent': u'box-python-sdk-1.5.0'},
 'params': None}
{"type":"user","id":"..","name":"Jeffrey Meadows","login":"..",..}
<boxsdk.object.user.User at 0x10615b8d0>
```

## Developer Token Client

The Box Developer Console allows for the creation of short-lived
developer tokens. The SDK makes it easy to use these tokens. Use the
`get_new_token_callback` parameter to control how the client will get
new developer tokens as needed. The default is to prompt standard input
for a token.

## Development Client

For exploring the Box API, or to quickly get going using the SDK, the
`DevelopmentClient` class combines the `LoggingClient` with the
`DeveloperTokenClient`.

# Customization

## Custom Subclasses

Custom object subclasses can be defined:

``` pycon
from boxsdk import Client
from boxsdk import Folder

class MyFolderSubclass(Folder):
    pass

client = Client(oauth)
client.translator.register('folder', MyFolderSubclass)
folder = client.folder('0')

>>> print folder
>>> <Box MyFolderSubclass - 0>
```

If an object subclass is registered in this way, instances of this
subclass will be returned from all SDK methods that previously returned
an instance of the parent. See `BaseAPIJSONObjectMeta` and `Translator`
to see how the SDK performs dynamic lookups to determine return types.

# FIPS 140-2 Compliance

The Python SDK allows the use of FIPS 140-2 validated SSL libraries, such as OpenSSL 3.0.
However, some actions are required to enable this functionality.

Currently, the latest distributions of Python default to OpenSSL v1.1.1, which is not FIPS compliant.
Therefore, if you want to use OpenSSL 3.0 in your network communication,
you need to ensure that Python uses a custom SSL library.
One way to achieve this is by creating a custom Python distribution with the ssl module replaced.

If you are using JWT for authentication, it is also necessary to ensure that the cryptography library,
which is one of the extra dependencies for JWT, uses OpenSSL 3.0.
To enable FIPS mode for the `cryptography` library, you need to install a FIPS-compliant version of OpenSSL
during the installation process of cryptography using the `pip` command.

# Versions
We use a modified version of [Semantic Versioning](https://semver.org/) for all changes. See [version strategy](VERSIONS.md) for details which is effective from 30 July 2022.

## Supported Version

Only the current MAJOR version of SDK is supported. New features, functionality, bug fixes, and security updates will only be added to the current MAJOR version.

A current release is on the leading edge of our SDK development, and is intended for customers who are in active development and want the latest and greatest features.  Instead of stating a release date for a new feature, we set a fixed minor or patch release cadence of maximum 2-3 months (while we may release more often). At the same time, there is no schedule for major or breaking release. Instead, we will communicate one quarter in advance the upcoming breaking change to allow customers to plan for the upgrade. We always recommend that all users run the latest available minor release for whatever major version is in use. We highly recommend upgrading to the latest SDK major release at the earliest convenient time and before the EOL date.

## Version schedule

| Version | Supported Environments                                  | State     | First Release | EOL/Terminated |
|---------|---------------------------------------------------------|-----------|---------------|----------------|
| 3       | Python 3.6+                                             | Supported | 17 Jan 2022   | TBD            |
| 2       |                                                         | EOL       | 01 Nov 2018   | 17 Jan 2022    |
| 1       |                                                         | EOL       | 10 Feb 2015   | 01 Nov 2018    |

# Contributing

See
[CONTRIBUTING.md](https://github.com/box/box-python-sdk/blob/main/CONTRIBUTING.md).

## Developer Setup

Create a virtual environment and install packages -

``` console
mkvirtualenv boxsdk
pip install -r requirements-dev.txt
```

## Testing

Run all tests using -

``` console
tox
```

The tox tests include code style checks via pep8 and pylint.

The tox tests are configured to run on Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11
and PyPy (our CI is configured to run PyPy tests on pypy-3.6, pypy-3.7, pypy-3.8).

# Questions, Bugs, and Feature Requests?

Need to contact us directly? [Browse the issues
tickets](https://github.com/box/box-python-sdk/issues)! Or, if that
doesn't work, [file a new
one](https://github.com/box/box-python-sdk/issues/new) and we will get
back to you. If you have general questions about the Box API, you can
post to the [Box Developer
Forum](https://community.box.com/t5/Developer-Forum/bd-p/DeveloperForum).

# Copyright and License

    Copyright 2019 Box, Inc. All rights reserved.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
