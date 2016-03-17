box-python-sdk
==============

.. image:: http://opensource.box.com/badges/active.svg
    :target: http://opensource.box.com/badges

.. image:: https://travis-ci.org/box/box-python-sdk.png?branch=master
    :target: https://travis-ci.org/box/box-python-sdk

.. image:: https://readthedocs.org/projects/box-python-sdk/badge/?version=latest
    :target: http://box-python-sdk.readthedocs.org/en/latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/boxsdk.svg
    :target: https://pypi.python.org/pypi/boxsdk

.. image:: https://img.shields.io/pypi/dm/boxsdk.svg
    :target: https://pypi.python.org/pypi/boxsdk



.. contents:: :depth: 1



Installing
----------

.. code-block:: console

    pip install boxsdk


Authorization
-------------

The Box API uses OAuth2 for auth. The SDK makes it relatively painless
to work with OAuth2 tokens.

Get the authorization url
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from boxsdk import OAuth2

    oauth = OAuth2(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        store_tokens=your_store_tokens_callback_method,
    )

    auth_url, csrf_token = oauth.get_authorization_url('http://YOUR_REDIRECT_URL')

store_tokens is a callback used to store the access token and refresh
token. You might want to define something like this:

.. code-block:: python

    def store_tokens(access_token, refresh_token):
        # store the tokens at secure storage (e.g. Keychain)

The SDK will keep the tokens in memory for the duration of the Python
script run, so you don't always need to pass store_tokens.

Authenticate (get access/refresh token)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you navigate the user to the auth_url, the user will eventually get
redirected to http://YOUR_REDIRECT_URL?code=YOUR_AUTH_CODE.  After
getting the code, you will be able to use the code to exchange for an
access token and refresh token.

The SDK handles all the work for you; all you need to do is run:

.. code-block:: python

    # Make sure that the csrf token you get from the `state` parameter
    # in the final redirect URI is the same token you get from the
    # get_authorization_url method.
    assert 'THE_CSRF_TOKEN_YOU_GOT' == csrf_token
    access_token, refresh_token = oauth.authenticate('YOUR_AUTH_CODE')

Create an authenticated client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from boxsdk import Client

    client = Client(oauth)

And that's it! You can start using the client to do all kinds of cool stuff
and the SDK will handle the token refresh for you automatically.

Usage
-----

Get user info
~~~~~~~~~~~~~

.. code-block:: python

    me = client.user(user_id='me').get()
    print 'user_login: ' + me['login']

Get folder info
~~~~~~~~~~~~~~~

.. code-block:: python

    root_folder = client.folder(folder_id='0').get()
    print 'folder owner: ' + root_folder.owned_by['login']
    print 'folder name: ' + root_folder['name']

Get items in a folder
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    items = client.folder(folder_id='0').get_items(limit=100, offset=0)

Create subfolder
~~~~~~~~~~~~~~~~

.. code-block:: python

    # creates folder structure /L1/L2/L3
    client.folder(folder_id='0').create_subfolder('L1').create_subfolder('L2').create_subfolder('L3')

Get shared link (file or folder)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    shared_link = client.folder(folder_id='SOME_FOLDER_ID').get_shared_link()

Get shared link direct download URL (files only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    download_url = client.file(file_id='SOME_FILE_ID').get_shared_link_download_url()

Get file name
~~~~~~~~~~~~~

.. code-block:: python

    client.file(file_id='SOME_FILE_ID').get()['name']

Rename an item
~~~~~~~~~~~~~~

.. code-block:: python

    client.file(file_id='SOME_FILE_ID').rename('bar-2.txt')

Move an item
~~~~~~~~~~~~

.. code-block:: python

    client.file(file_id='SOME_FILE_ID').move(client.folder(folder_id='SOME_FOLDER_ID'))

Get content of a file
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client.file(file_id='SOME_FILE_ID').content()

Lock/unlock a file
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client.file(file_id='SOME_FILE_ID').lock()
    client.file(file_id='SOME_FILE_ID').unlock()

Search
~~~~~~

.. code-block:: python

    client.search('some_query', limit=100, offset=0)

Metadata Search
~~~~~~~~~~~~~~~

.. code-block:: python

    from boxsdk.object.search import MetadataSearchFilter, MetadataSearchFilters

    metadata_search_filter = MetadataSearchFilter(template_key='marketingCollateral', scope='enterprise')
    metadata_search_filter.add_value_based_filter(field_key='documentType', value='datasheet')
    metadata_search_filter.add_value_based_filter(field_key='clientNumber', value='a123')

    metadata_search_filters = MetadataSearchFilters()
    metadata_search_filters.add_filter(metadata_search_filter)

    client.search('some_query', limit=100, offset=0, metadata_filters=metadata_search_filters)

Events
~~~~~~

.. code-block:: python

    # Get events
    client.events().get_events(limit=100, stream_position='now')

    # Generate events using long polling
    for event in client.events().generate_events_with_long_polling():
        pass  # Do something with the event

    # Get latest stream position
    client.events().get_latest_stream_position()

Metadata
~~~~~~~~

.. code-block:: python

    # Get metadata
    client.file(file_id='SOME_FILE_ID').metadata().get()

    # Create metadata
    client.file(file_id='SOME_FILE_ID').metadata().create({'key': 'value'})

    # Update metadata
    metadata = client.file(file_id='SOME_FILE_ID').metadata()
    update = metadata.start_update()
    update.add('/key', 'new_value')
    metadata.update(update)

As-User
~~~~~~~

The ``Client`` class and all Box objects also have an ``as_user`` method.

``as-user`` returns a copy of the object on which it was called that will make Box API requests
as though the specified user was making it.

See https://box-content.readme.io/#as-user-1 for more information about how this works via the Box API.

.. code-block:: python

    # Logged in as admin, but rename a file as SOME USER
    user = client.user(user_id='SOME_USER_ID')
    client.as_user(user).file(file_id='SOME_FILE_ID').rename('bar-2.txt')


    # Same thing, but using file's as_user method
    client.file(file_id='SOME_FILE_ID').as_user(user).rename('bar-2.txt')

Other Requests
~~~~~~~~~~~~~~

The Box API is continually evolving. As such, there are API endpoints available that are not specifically
supported by the SDK. You can still use these endpoints by using the ``make_request`` method of the ``Client``.

.. code-block:: python

    # https://box-content.readme.io/reference#get-metadata-schema
    # Returns a Python dictionary containing the result of the API request
    json_response = client.make_request(
        'GET',
        client.get_url('metadata_templates', 'enterprise', 'customer', 'schema'),
    ).json()

``make_request()`` takes two parameters:

- ``method`` -an HTTP verb like ``GET`` or ``POST``
- ``url`` - the URL of the requested API endpoint

The ``Client`` class and Box objects have a ``get_url`` method. Pass it an endpoint
to get the correct URL for use with that object and endpoint.

Box Developer Edition
---------------------

The Python SDK supports your
`Box Developer Edition <https://box-content.readme.io/docs/app-users/>`__ applications.

Developer Edition support requires some extra dependencies. To get them, simply

.. code-block:: console

    pip install boxsdk[jwt]

Instead of instantiating your ``Client`` with an instance of ``OAuth2``,
instead use an instance of ``JWTAuth``.

.. code-block:: python

    from boxsdk import JWTAuth

    auth = JWTAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        enterprise_id='YOUR_ENTERPRISE_ID',
        jwt_key_id='YOUR_JWT_KEY_ID',
        rsa_private_key_file_sys_path='CERT.PEM',
        store_tokens=your_store_tokens_callback_method,
    )

    access_token = auth.authenticate_instance()

    from boxsdk import Client

    client = Client(auth)

This client is able to create application users:

.. code-block:: python

    ned_stark_user = client.create_user('Ned Stark')

These users can then be authenticated:

.. code-block:: python

    ned_auth = JWTAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        enterprise_id='YOUR_ENTERPRISE_ID',
        jwt_key_id='YOUR_JWT_KEY_ID',
        rsa_private_key_file_sys_path='CERT.PEM',
        store_tokens=your_store_tokens_callback_method,
    )
    ned_auth.authenticate_app_user(ned_stark_user)
    ned_client = Client(ned_auth)

Requests made with ``ned_client`` (or objects returned from ``ned_client``'s methods)
will be performed on behalf of the newly created app user.

Other Auth Options
------------------

For advanced uses of the SDK, two additional auth classes are provided:

- ``CooperativelyManagedOAuth2``: Allows multiple auth instances to share tokens.
- ``RemoteOAuth2``: Allows use of the SDK on clients without access to your application's client secret. Instead, you
  provide a ``retrieve_access_token`` callback. That callback should perform the token refresh, perhaps on your server
  that does have access to the client secret.
- ``RedisManagedOAuth2``: Stores access and refresh tokens in Redis. This allows multiple processes (possibly spanning
  multiple machines) to share access tokens while synchronizing token refresh. This could be useful for a multiprocess
  web server, for example.

Other Client Options
--------------------

Logging Client
~~~~~~~~~~~~~~

For more insight into the network calls the SDK is making, you can use the ``LoggingClient`` class. This class logs
information about network requests and responses made to the Box API.

.. code-block:: pycon

    >>> from boxsdk import LoggingClient
    >>> client = LoggingClient()
    >>> client.user().get()
    GET https://api.box.com/2.0/users/me {'headers': {u'Authorization': u'Bearer ---------------------------kBjp',
                 u'User-Agent': u'box-python-sdk-1.5.0'},
     'params': None}
    {"type":"user","id":"..","name":"Jeffrey Meadows","login":"..",..}
    <boxsdk.object.user.User at 0x10615b8d0>

For more control over how the information is logged, use the ``LoggingNetwork`` class directly.

.. code-block:: pycon

    from boxsdk import Client
    from boxsdk.network.logging_network import LoggingNetwork

    # Use a custom logger
    client = Client(oauth, network_layer=LoggingNetwork(logger))

Developer Token Client
~~~~~~~~~~~~~~~~~~~~~~

The Box Developer Console allows for the creation of short-lived developer tokens. The SDK makes it easy to use these
tokens. Use the ``get_new_token_callback`` parameter to control how the client will get new developer tokens as
needed. The default is to prompt standard input for a token.

Development Client
~~~~~~~~~~~~~~~~~~

For exploring the Box API, or to quickly get going using the SDK, the ``DevelopmentClient`` class combines the
``LoggingClient`` with the ``DeveloperTokenClient``.

Contributing
------------

See `CONTRIBUTING.rst <https://github.com/box/box-python-sdk/blob/master/CONTRIBUTING.rst>`_.


Developer Setup
~~~~~~~~~~~~~~~

Create a virtual environment and install packages -

.. code-block:: console

    mkvirtualenv boxsdk
    pip install -r requirements-dev.txt


Testing
~~~~~~~

Run all tests using -

.. code-block:: console

    tox

The tox tests include code style checks via pep8 and pylint.

The tox tests are configured to run on Python 2.6, 2.7, 3.3, 3.4, 3.5, and
PyPy (our CI is configured to run PyPy tests on PyPy 4.0).


Support
-------

Need to contact us directly? Email oss@box.com and be sure to include the name
of this project in the subject. For questions, please contact us directly
rather than opening an issue.


Copyright and License
---------------------

::

 Copyright 2015 Box, Inc. All rights reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
