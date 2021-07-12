.. boxsdk documentation main file, created by
   sphinx-quickstart on Tue Dec 16 01:10:30 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Box Python SDK
==============


Installing
----------

.. code-block:: console

    pip install boxsdk


Source Code
-----------

https://github.com/box/box-python-sdk


Quickstart
----------

Create a developer token from your app's configuration page (https://app.box.com/developers/services).

You'll be prompted for it on the command line.

.. code-block:: pycon

    $ from boxsdk import DevelopmentClient
    $ client = DevelopmentClient()
    >>> Enter developer token: <enter your developer token>
    $ me = client.user().get()

    GET https://api.box.com/2.0/users/me {'headers': {u'Authorization': u'Bearer ----KkeV',
                 u'User-Agent': u'box-python-sdk-1.4.3'},
     'params': None}

    {"type":"user","id":"----6009","name":"Jeffrey Meadows","login":"jmeadows@box.com",...}

    $ me.name
    >>> Jeffrey Meadows

The ``DevelopmentClient`` uses Box developer tokens for auth (and will prompt you for a new token upon
expiration), and logs API requests and responses, making it really easy to get started learning the SDK and Box API.


Creating an App for Users
-------------------------

Authorization
~~~~~~~~~~~~~

If you'd like other users to use your app, you need to set up a way for them to authorize your app and
grant it access to their Box account. The ``auth`` module contains several classes to help you do that.

The simplest class is the ``OAuth2`` class. To use it, instantiate it with your ``client_id`` and ``client_secret``.

Follow the `tutorial on GitHub <https://github.com/box/box-python-sdk/blob/main/README.rst#id2>`_ for
instructions on how to get an authorized client for a user. Using the ``store_tokens`` callback, you may persist
the user's auth and refresh tokens for the next time they use your app. Once they return to your app, you can
create an authorized client like so:

.. code-block:: python

    from boxsdk import OAuth2, Client

    oauth = OAuth2(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        store_tokens=your_store_tokens_callback_method,
        access_token=persisted_access_token,
        refresh_token=persisted_refresh_token,
    )
    client = Client(oauth)


Making requests to Box
~~~~~~~~~~~~~~~~~~~~~~

Once you have an authorized client, you can use it to make requests to Box on your user's behalf. The client
has several methods to help you get started, many of which return Box objects, which, in turn, have methods that
correspond to Box API endpoints.

The module documentation below describes each of these methods and which parameters they require. Some API endpoints
do not have corresponding SDK methods; for those, you can use the generic ``make_request`` method of the client.

Module Documentation
--------------------

.. toctree::
    :maxdepth: 4

    boxsdk


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

