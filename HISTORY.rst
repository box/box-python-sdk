.. :changelog:

Release History
---------------

3.0.1 (2022-01-26)
++++++++++++++++++++

**Bug Fixes:**

- Move sphinx to test requirements (`#662 <https://github.com/box/box-python-sdk/pull/662>`_)

3.0.0 (2022-01-17)
++++++++++++++++++++

**Breaking Changes**

- Drop support for python 2.7 (`#645 <https://github.com/box/box-python-sdk/pull/645>`_)
- Add missing parameter stream_position to get_admin_events method (`#648 <https://github.com/box/box-python-sdk/pull/648>`_)
- Drop support for python 3.5 (`#654 <https://github.com/box/box-python-sdk/pull/654>`_)
- Remove deprecated code using insensitive language (`#651 <https://github.com/box/box-python-sdk/pull/651>`_)
- Enforcing usage of keyword-only arguments in some functions (`#656 <https://github.com/box/box-python-sdk/pull/656>`_)

**New Features and Enhancements:**

- Remove six library and __future__ imports (`#646 <https://github.com/box/box-python-sdk/pull/646>`_)
- Add type hints to method parameters (`#650 <https://github.com/box/box-python-sdk/pull/650>`_)

**Bug Fixes:**

- Add missing api_call decorators on multiput calls (`#653 <https://github.com/box/box-python-sdk/pull/653>`_)
- Added `py.typed` file for mypy to recognise type hints (`#657 <https://github.com/box/box-python-sdk/pull/657>`_)

2.14.0 (2021-12-08)
++++++++++++++++++++

**New Features and Enhancements:**

- Add `admin_logs_streaming` support for events stream (`#623 <https://github.com/box/box-python-sdk/pull/623>`_)
- Add `vanity_name` parameter for creating shared link to a file or folder (`#637 <https://github.com/box/box-python-sdk/pull/637>`_)
- Add getting files and file versions under retention for a retention policy assignment (`#633 <https://github.com/box/box-python-sdk/pull/633>`_)
- Support base item operations for WebLink class (`#639 <https://github.com/box/box-python-sdk/pull/639>`_)

**Bug Fixes:**

- Limit cryptography to version <3.5.0 (`#636 <https://github.com/box/box-python-sdk/pull/636>`_)
- Avoid raising 404 when a thumbnail cannot be generated for a file (`#642 <https://github.com/box/box-python-sdk/pull/642>`_)

2.13.0 (2021-09-30)
++++++++++++++++++++

**New Features and Enhancements:**

- Sensitive language replacement (`#609 <https://github.com/box/box-python-sdk/pull/609>`_)
- Add BoxSign support (`#617 <https://github.com/box/box-python-sdk/pull/617>`_)

**Bug Fixes:**

- Upgrade cryptography to version 3 (`#620 <https://github.com/box/box-python-sdk/pull/620>`_)

2.12.1 (2021-06-16)
++++++++++++++++++++

**Bug Fixes:**

- Fix bug when thumbnail representations are not found (`#597 <https://github.com/box/box-python-sdk/pull/597>`_)

2.12.0 (2021-04-16)
++++++++++++++++++++

**New Features and Enhancements:**

- Add metadata query functionality (`#574 <https://github.com/box/box-python-sdk/pull/574>`_)
- Add folder lock functionality (`#581 <https://github.com/box/box-python-sdk/pull/581>`_)
- Add search query support for the `include_recent_shared_links` field  (`#582 <https://github.com/box/box-python-sdk/pull/582>`_)
- Update `get_groups()` to use documented parameter to filter by name (`#586 <https://github.com/box/box-python-sdk/pull/586>`_)

2.11.0 (2021-01-11)
++++++++++++++++++++

**New Features and Enhancements:**

- Deprecate and add method for getting a thumbnail (`#572 <https://github.com/box/box-python-sdk/pull/572>`_)

2.10.0 (2020-10-02)
++++++++++++++++++++

**New Features and Enhancements:**

- Add support for `copyInstanceOnItemCopy` field for metadata templates (`#546 <https://github.com/box/box-python-sdk/pull/546>`_)
- Allow creating tasks with the `action` and `completion_rule` parameters (`#544 <https://github.com/box/box-python-sdk/pull/544>`_)
- Add zip functionality (`#539 <https://github.com/box/box-python-sdk/pull/539>`_)

**Bug Fixes:**

- Fix bug with updating a collaboration role to owner (`#536 <https://github.com/box/box-python-sdk/pull/536>`_)
- Allow ints to be passed in as item IDs (`#530 <https://github.com/box/box-python-sdk/pull/530>`_)

2.9.0 (2020-06-23)
++++++++++++++++++++
- Fix exception handling for OAuth
- Fix path parameter sanitization

2.8.0 (2020-04-24)
++++++++++++++++++++
- Added support for token exchange using shared links
- Added the ability to pass in a SHA1 value for file uploads

2.7.1 (2020-01-21)
++++++++++++++++++++
- Fixed bug in `_get_retry_request_callable` introduced in release 2.7.0 which caused chunked uploads to fail

2.7.0 (2020-01-16)
++++++++++++++++++++
- Fixed bug in `get_admin_events` function which caused errors when the optional `event_types` parameter was omitted.
- Add marker based pagination for listing users.
- Added support for more attribute parameters when uploading new files and new versions of existing files.
- Combined preflight check and lookup of accelerator URL into a single request for uploads.
- Fixed JWT retry logic so a new JTI claim is generated on each retry.
- Fixed bug where JWT authentication requests returned incorrect error codes.
- Fixed retry logic so when a `Retry-After` header is passed back from the API, the SDK waits for the amount of time specified in the header before retrying.

2.6.1 (2019-10-24)
++++++++++++++++++
- Added `api_call` decorator for copy method.

2.6.0 (2019-08-29)
++++++++++++++++++
- Added a new get events function with created_before, created_after, and event_type parameters

2.5.0 (2019-06-20)
++++++++++++++++++
- Allowed passing `None` to clear configurable_permission field in the add_member() method.

2.4.1 (2019-05-16)
++++++++++++++++++

- Patch release for issues with v2.4.0.

2.4.0 (2019-05-16)
++++++++++++++++++

- Added ability to set metadata on a `file <https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#set-metadata>`_ or a `folder <https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#set-metadata>`_

2.3.2 (2019-03-29)
++++++++++++++++++

- Fixing an issue in v2.3.1 where package could not be installed.

2.3.1 (2019-03-29)
++++++++++++++++++

- Fixing an issue in v2.3.0 where package could not be installed.

2.3.0 (2019-03-28)
++++++++++++++++++

- Added the ability to set `file description upon upload <https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#upload-a-file>`_
- Added support for `basic authenticated proxy and unauthenticated proxy <https://github.com/box/box-python-sdk/blob/main/docs/usage/configuration.md#proxy>`_

2.2.2 (2019-03-14)
++++++++++++++++++

- Updated requests-toolbelt dependency restriction.

2.2.1 (2019-02-15)
++++++++++++++++++

- Fixing an issue in v2.2.0 where package could not be installed.

2.2.0 (2019-02-14)
++++++++++++++++++

- Added abilty for user to `retrieve an avatar <https://github.com/box/box-python-sdk/blob/main/docs/usage/user.md#get-the-avatar-for-a-user>`_
  for a user.
- Changed retry strategy to use exponential backoff with randomized jitter.

2.1.0 (2019-02-07)
++++++++++++++++++

- Added ability for user to `chunk upload files <https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#chunked-upload>`_
  and resume uploads for interrupted uploads.
- Added ability to `verify webhook message <https://github.com/box/box-python-sdk/blob/main/docs/usage/webhook.md#validate-webhook-message>`_.
- Added ability for user to add metadata classification to `files <https://github.com/box/box-python-sdk/blob/main/docs/usage/files.md#set-a-classification>`_ 
  and `folders <https://github.com/box/box-python-sdk/blob/main/docs/usage/folders.md#set-a-classification>`_.
- Bugfix where calling  ``.response_object()`` method on an API object could throw.

2.0.0
++++++++++++++++

**Breaking Changes**

- Python 2.6 is no longer supported.
- Python 3.3 is no longer supported.
- ``client.search()`` now returns a ``Search`` object that exposes a ``query()`` method to call the Search API.
  Use ``client.search().query(**search_params)`` instead of ``client.search(**search_params)``.
- ``client.get_memberships(...)`` has a change in signature. The limit and offset parameters have swapped positions to keep
  consistency with the rest of the SDK.
- ``client.groups(...)`` has been changed to ``client.get_groups``. The limit and offset parameters have swapped positions.
- The ``unshared_at`` parameter for ``item.create_shared_link(...)`` and ``file.get_shared_link_download_url(...)``
  now takes an `RFC3339-formatted <https://tools.ietf.org/html/rfc3339#section-5.8>` ``unicode`` string instead of a
  ``datetime.date``.  Users migrating from v1.x can pass the value of ``date.isoformat()`` instead of the ``date``
  object itself.
- ``Events.get_events(...)`` now returns a list of ``Event`` instances rather than a list of ``dict``
  representing events.  ``Event`` inherits from ``Mapping`` but will not have all the same capabilities as
  ``dict``.

  + Your code is affected if you use ``Events.get_events(...)`` and expect a list of ``dict`` rather than a list of
    ``Mapping``.  For example, if you use ``__setitem__`` (``event['key'] = value``), ``update()``, ``copy()``, or
    if your code depends on the ``str`` or ``repr`` of the ``Event``.  Use of ``__getitem__`` (``event['key']``),
    ``get()``, and other ``Mapping`` methods is unaffected.  See
    https://docs.python.org/2.7/library/collections.html#collections-abstract-base-classes for methods supported on
    ``Mapping`` instances.

  + Migration: If you still need to treat an ``Event`` as a ``dict``, you can get a deepcopy of the original ``dict``
    using the new property on ``BaseAPIJSONObject``, ``response_object``.

- ``LoggingNetwork`` has been removed. Logging calls are now made from the ``DefaultNetwork`` class. In addition,
  the logging format strings in this class have changed in a way that
  will break logging for any applications that have overridden any of these
  strings. They now use keyword format placeholders instead of positional
  placeholders. All custom format strings will now have to use the same keyword
  format placeholders. Though this is a breaking change, the good news is that
  using keyword format placeholders means that any future changes will be
  automatically backwards-compatibile (as long as there aren't any changes to
  change/remove any of the keywords).

- ``File.update_contents()`` and ``File.update_contents_with_stream()`` now
  correctly return a ``File`` object with the correct internal JSON structure.
  Previously it would return a ``File`` object where the file JSON is hidden
  inside ``file['entries'][0]``. This is a bugfix, but will be a breaking
  change for any clients that have already written code to handle the bug.

- Comparing two objects (e.g. a ``File`` and a ``Folder``) that have the same Box ID but different types with ``==``
  will now correctly return `False`.

- The following methods now return iterators over the entire collection of returned objects, rather than
  a single page:

  + ``client.users()``
  + ``client.groups()``
  + ``client.search().query()``
  + ``folder.get_items()``

  Since ``folder.get_items()`` now returns an iterator, ``folder.get_items_limit_offset()`` and
  ``folder.get_items_marker()`` have been removed.  To use marker based paging with ``folder.get_items()``,
  pass the ``use_marker=True`` parameter and optionally specify a ``marker`` parameter to begin paging from that
  point in the collection.

  Additionally, ``group.membership()`` has been renamed to ``group.get_memberships()``, and returns an iterator of
  membership objects.  This method no longer provides the option to return tuples with paging information.

- The ``Translator`` class has been reworked; ``translator.get(...)`` still returns the constructor for the object class
  corresponding to the passed in type, but ``translator.translate(...)`` now takes a ``Session`` and response object
  directly and produces the translated object.  This method will also translate any nested objects found.

  + This change obviates the need for ``GroupMembership`` to have a custom constructor; it now uses the default
    ``BaseObject`` constructor.

**Features**

- All publicly documented API endpoints and parameters should now be supported by the SDK
- Added more flexibility to the object translation system:

  - Can create non-global ``Translator`` instances, which can extend or
    not-extend the global default ``Translator``.
  - Can initialize ``BoxSession`` with a custom ``Translator``.
  - Can register custom subclasses on the ``Translator`` which is associated
    with a ``BoxSession`` or a ``Client``.
  - All translation of API responses now use the ``Translator`` that is
    referenced by the ``BoxSession``, instead of directly using the global
    default ``Translator``.
  - Nested objects are now translated by ``translator.translate()``

- When the ``auto_session_renewal`` is ``True`` when calling any of the request
  methods on ``BoxSession``, if there is no access token, ``BoxSession`` will
  renew the token _before_ making the request. This saves an API call.
- Auth objects can now be closed, which prevents them from being used to
  request new tokens. This will also revoke any existing tokens (though that
  feature can be disabled by passing ``revoke=False``). Also introduces a
  ``closing()`` context manager method, which will auto-close the auth object
  on exit.
- Various enhancements to the ``JWTAuth`` baseclass:

  - The ``authenticate_app_user()`` method is renamed to
    ``authenticate_user()``, to reflect that it may now be used to authenticate
    managed users as well. See the method docstring for details.
    ``authenticate_app_user()`` is now an alias of ``authenticate_user()``, in
    order to not introduce an unnecessary backwards-incompatibility.
  - The ``user`` argument to ``authenticate_user()`` may now be either a user
    ID string or a ``User`` instance. Before it had to be a ``User`` instance.
  - The constructor now accepts an optional ``user`` keyword argument, which
    may be a user ID string or a ``User`` instance. When this is passed,
    ``authenticate_user()`` and can be called without passing a value for the
    ``user`` argument. More importantly, this means that ``refresh()`` can be
    called immediately after construction, with no need for a manual call to
    ``authenticate_user()``. Combined with the aforementioned improvement to
    the ``auto_session_renewal`` functionality of ``BoxSession``, this means
    that authentication for ``JWTAuth`` objects can be done completely
    automatically, at the time of first API call.
  - The constructor now supports passing the RSA private key in two different
    ways: by file system path (existing functionality), or by passing the key
    data directly (new functionality). The ``rsa_private_key_file_sys_path``
    parameter is now optional, but it is required to pass exactly one of
    ``rsa_private_key_file_sys_path`` or ``rsa_private_key_data``.
  - Document that the ``enterprise_id`` argument to ``JWTAuth`` is allowed to
    be ``None``.
  - ``authenticate_instance()`` now accepts an ``enterprise`` argument, which
    can be used to set and authenticate as the enterprise service account user,
    if ``None`` was passed for ``enterprise_id`` at construction time.
  - Authentications that fail due to the expiration time not falling within the
    correct window of time are now automatically retried using the time given
    in the Date header of the Box API response. This can happen naturally when
    the system time of the machine running the Box SDK doesn't agree with the
    system time of the Box API servers.

- Added an ``Event`` class.
- Moved ``metadata()`` method to ``Item`` so it's now available for ``Folder``
  as well as ``File``.
- The ``BaseAPIJSONObject`` baseclass (which is a superclass of all API
  response objects) now supports ``__contains__`` and ``__iter__``. They behave
  the same as for ``Mapping``. That is, ``__contains__`` checks for JSON keys
  in the object, and ``__iter__`` yields all of the object's keys.

- Added a ``RecentItem`` class.
- Added ``client.get_recent_items()`` to retrieve a user's recently accessed items on Box.
- Added support for the ``can_view_path`` parameter when creating new collaborations.
- Added ``BoxObjectCollection`` and subclasses ``LimitOffsetBasedObjectCollection`` and
  ``MarkerBasedObjectCollection`` to more easily manage paging of objects from an endpoint.
  These classes manage the logic of constructing requests to an endpoint and storing the results,
  then provide ``__next__`` to easily iterate over the results. The option to return results one
  by one or as a ``Page`` of results is also provided.
- Added a ``downscope_token()`` method to the ``Client`` class. This generates a token that
  has its permissions reduced to the provided scopes and for the optionally provided 
  ``File`` or ``Folder``.
- Added methods for configuring ``JWTAuth`` from config file: ``JWTAuth.from_settings_file`` and
  ``JWTAuth.from_settings_dictionary``.
- Added ``network_response`` property to ``BoxOAuthException``.
- API Configuration can now be done per ``BoxSession`` instance.

**Other**

- Added extra information to ``BoxAPIException``.
- Added ``collaboration()`` method to ``Client``.
- Reworked the class hierarchy.  Previously, ``BaseEndpoint`` was the parent of ``BaseObject`` which was the parent
  of all smart objects.  Now ``BaseObject`` is a child of both ``BaseEndpoint`` and ``BaseAPIJSONObject``.
  ``BaseObject`` is the parent of all objects that are a part of the REST API.  Another subclass of
  ``BaseAPIJSONObject``, ``APIJSONObject``, was created to represent pseudo-smart objects such as ``Event`` that are not
  directly accessible through an API endpoint.
- Added ``network_response_constructor`` as an optional property on the
  ``Network`` interface. Implementations are encouraged to override this
  property, and use it to construct ``NetworkResponse`` instances. That way,
  subclass implementations can easily extend the functionality of the
  ``NetworkResponse``, by re-overriding this property. This property is defined
  and used in the ``DefaultNetwork`` implementation.
- Move response logging to a new ``LoggingNetworkResponse`` class (which is
  made possible by the aforementioned ``network_response_constructor``
  property). Now the SDK decides whether to log the response body, based on
  whether the caller reads or streams the content.
- Add more information to the request/response logs from ``LoggingNetwork``.
- Add logging for request exceptions in ``LoggingNetwork``.
- Bugfix so that the return value of ``JWTAuth.refresh()`` correctly matches
  that of the auth interface (by returning a tuple of
  ((access token), (refresh token or None)), instead of just the access token).
  In particular, this fixes an exception in ``BoxSession`` that always occurred
  when it tried to refresh any ``JWTAuth`` object.
- Fixed an exception that was being raised from ``ExtendableEnumMeta.__dir__()``.
- CPython 3.6 support.
- Increased required minimum version of six to 1.9.0.

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
- Added support for 'As-User' requests. See https://developer.box.com/en/guides/authentication/oauth2/as-user/
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
