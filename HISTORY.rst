.. :changelog:

Release History
---------------

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