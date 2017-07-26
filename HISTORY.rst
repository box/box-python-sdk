.. :changelog:

Release History
---------------

Upcoming
++++++++

1.5.4
++++++++++++++++++

- Bugfix so that the return value of ``JWTAuth.refresh()`` correctly matches
  that of the auth interface (by returning a tuple of
  ((access token), (refresh token or None)), instead of just the access token).
  In particular, this fixes an exception in ``BoxSession`` that always occurred
  when it tried to refresh any ``JWTAuth`` object.
- Fixed an exception that was being raised from ``ExtendableEnumMeta.__dir__()``.
- CPython 3.6 support.

1.5.3 (2016-05-26)
++++++++++++++++++

- Bugfix so that ``JWTAuth`` opens the PEM private key file in ``'rb'`` mode.

1.5.2 (2016-05-19)
++++++++++++++++++

- Bugfix so that ``OAuth2`` always has the correct tokens after a call to ``refresh()``.

1.5.1 (2016-03-23)
++++++++++++++++++

- Added a ``revoke()`` method to the ``OAuth2`` class. Calling it will revoke the current access/refresh token pair.


1.5.0 (2016-03-17)
++++++++++++++++++

- Added a new class, ``LoggingClient``. It's a ``Client`` that uses the ``LoggingNetwork`` class so that
  requests to the Box API and its responses are logged.
- Added a new class, ``DevelopmentClient`` that combines ``LoggingClient`` with the existing
  ``DeveloperTokenClient``. This client is ideal for exploring the Box API or for use when developing your application.
- Made the ``oauth`` parameter to ``Client`` optional. The constructor now accepts new parameters that it will use
  to construct the ``OAuth2`` instance it needs to auth with the Box API.
- Changed the default User Agent string sent with requests to the Box API. It is now 'box-python-sdk-<version>'.
- Box objects have an improved ``__repr__``, making them easier to identify during debugging sessions.
- Box objects now implement ``__dir__``, making them easier to explore. When created with a Box API response,
  these objects will now include the API response fields as attributes.



1.4.2 (2016-02-23)
++++++++++++++++++

- Make sure that ``__all__`` is only defined once, as a list of ``str``. Some
  programs (e.g. PyInstaller) naively parse __init__.py files, and if
  ``__all__`` is defined twice, the second one will be ignored. This can cause
  ``__all__`` to appear as a list of ``unicode`` on Python 2.
- Create wheel with correct conditional dependencies and license file.
- Change the ``license`` meta-data from the full license text, to just a short
  string, as specified in [1][2].

  [1] <https://docs.python.org/3.5/distutils/setupscript.html#additional-meta-data>

  [2] <https://www.python.org/dev/peps/pep-0459/#license>

- Include entire test/ directory in source distribution. test/__init__.py was
  previously missing.
- Update documentation.

1.4.1 (2016-02-11)
++++++++++++++++++

- Files now support getting a direct download url.

1.4.0 (2016-01-05)
++++++++++++++++++

- Added key id parameter to JWT Auth.


1.3.3 (2016-01-04)
++++++++++++++++++

**Bugfixes**

- Fixed import error for installations that don't have redis installed.
- Fixed use of ``raw_input`` in the developer token auth for py3 compatibility.


1.3.3 (2015-12-22)
++++++++++++++++++

- Added a new class, ``DeveloperTokenClient`` that makes it easy to get started using the SDK with a Box developer
  token. It uses another new class, ``DeveloperTokenAuth`` for auth.

**Bugfixes**

- Added limit, offset, and filter_term parameters to ``client.users()`` to match up with the Box API.

1.3.2 (2015-11-16)
++++++++++++++++++

- Fix ``boxsdk.util.log.setup_logging()`` on Python 3.

1.3.1 (2015-11-06)
++++++++++++++++++

- Add requests-toolbelt to setup.py (it was accidentally missing from 1.3.0).

1.3.0 (2015-11-05)
++++++++++++++++++

- CPython 3.5 support.
- Support for cryptography>=1.0 on PyPy 2.6.
- Travis CI testing for CPython 3.5 and PyPy 2.6.0.
- Added a logging network class that logs requests and responses.
- Added new options for auth classes, including storing tokens in Redis and storing them on a remote server.
- Stream uploads of files from disk.

1.2.2 (2015-07-22)
++++++++++++++++++

- The SDK now supports setting a password when creating a shared link.

1.2.1 (2015-07-22)
++++++++++++++++++

**Bugfixes**

- Fixed an ImportError for installs that didn't install the [jwt] extras.

1.2.0 (2015-07-13)
++++++++++++++++++

- Added support for Box Developer Edition. This includes JWT auth (auth as enterprise or as app user),
  and ``create_user`` functionality.
- Added support for setting shared link expiration dates.
- Added support for setting shared link permissions.
- Added support for 'As-User' requests. See https://box-content.readme.io/#as-user-1
- Improved support for accessing shared items. Items returned from the ``client.get_shared_item`` method will
  remember the shared link (and the optionally provided shared link password) so methods called on the returned
  items will be properly authorized.

1.1.7 (2015-05-28)
++++++++++++++++++

- Add context_info from failed requests to BoxAPIException instances.

**Bugfixes**

- ``Item.remove_shared_link()`` was trying to return an incorrect (according to its own documentation) value, and was
  also attempting to calculate that value in a way that made an incorrect assumption about the API response. The latter
  problem caused invocations of the method to raise TypeError. The method now handles the response correctly, and
  correctly returns type ``bool``.

1.1.6 (2015-04-17)
++++++++++++++++++

- Added support for the Box accelerator API for premium accounts.

1.1.5 (2015-04-03)
++++++++++++++++++

- Added support for preflight check during file uploads and updates.

1.1.4 (2015-04-01)
++++++++++++++++++

- Added support to the search endpoint for metadata filters.
- Added support to the search endpoint for filtering based on result type and content types.

1.1.3 (2015-03-26)
++++++++++++++++++

- Added support for the /shared_items endpoint. ``client.get_shared_item`` can be used to get information about
  a shared link. See https://developers.box.com/docs/#shared-items

1.1.2 (2015-03-20)
++++++++++++++++++

**Bugfixes**

- Certain endpoints (e.g. search, get folder items) no longer raise an exception when the response contains items
  that are neither files nor folders.

1.1.1 (2015-03-11)
++++++++++++++++++

- A minor change to namespacing. The ``OAuth2`` class can now be imported directly from ``boxsdk``.
  Demo code has been updated to reflect the change.

1.1.0 (2015-03-02)
++++++++++++++++++

**Features**

- The SDK now supports Box metadata. See the `metadata docs <https://developers.box.com/metadata-api/>`_ for
  more information.

- The object paging API has been improved. SDK extensions that need fine-grained control over when the next "page"
  of API results will be fetched can now do that.

**Example Code**

- The example code has been improved to be more robust and to work with all Python versions supported by the SDK
  (CPython 2.6-2.7, CPython 3.3-3.4, and PyPy).

- The example code has an example on how to use the new metadata feature.

- The README has improved code examples.

**Bugfixes**

- Oauth2 redirect URIs containing non-ASCII characters are now supported.
