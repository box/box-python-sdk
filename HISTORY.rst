.. :changelog:

Release History
---------------

2.0.0 (Upcoming)
++++++++++++++++

**Breaking Changes**

- Python 2.6 is no longer supported.
- Python 3.3 is no longer supported.
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

**Features**

- Added more flexibility to the object translation system:

  - Can create non-global ``Translator`` instances, which can extend or
    not-extend the global default ``Translator``.
  - Can initialize ``BoxSession`` with a custom ``Translator``.
  - Can register custom subclasses on the ``Translator`` which is associated
    with a ``BoxSession`` or a ``Client``.
  - All translation of API responses now use the ``Translator`` that is
    referenced by the ``BoxSession``, instead of directly using the global
    default ``Translator``.

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
