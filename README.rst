box-python-sdk
==============

.. image:: http://opensource.box.com/badges/active.svg
    :target: http://opensource.box.com/badges

.. image:: https://travis-ci.org/box/box-python-sdk.png?branch=master
    :target: https://travis-ci.org/box/box-python-sdk

.. image:: https://readthedocs.org/projects/box-python-sdk/badge/?version=latest
    :target: http://box-python-sdk.readthedocs.org/en/latest
    :alt: Documentation Status

.. image:: https://pypip.in/v/boxsdk/badge.png
    :target: https://pypi.python.org/pypi/boxsdk

.. image:: https://pypip.in/d/boxsdk/badge.png
    :target: https://pypi.python.org/pypi/boxsdk


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
getting the code, you will be able to use the code to exchange for
access token and fresh token.

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

Get shared link
~~~~~~~~~~~~~~~

.. code-block:: python

    shared_link = client.folder(folder_id='SOME_FOLDER_ID').get_shared_link()

Get file name
~~~~~~~~~~~~~~~

.. code-block:: python

    client.file(file_id='SOME_FILE_ID').get()['name']

Rename an item
~~~~~~~~~~~~~~

.. code-block:: python

    client.file(file_id='SOME_FILE_ID').rename('bar-2.txt')

Move an item
~~~~~~~~~~~~~~

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

The tox tests are configured to run on Python 2.6, 2.7, 3.3, 3.4, and
PyPy.


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
