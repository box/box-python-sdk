# coding: utf-8

from __future__ import unicode_literals, absolute_import

from sys import version_info as py_version

from . import version


class API(object):
    """Configuration object containing the URLs for the Box API."""
    BASE_API_URL = 'https://api.box.com/2.0'
    UPLOAD_URL = 'https://upload.box.com/api/2.0'
    OAUTH2_API_URL = 'https://api.box.com/oauth2'  # <https://developers.box.com/docs/#oauth-2>
    OAUTH2_AUTHORIZE_URL = 'https://account.box.com/api/oauth2/authorize'  # <https://developers.box.com/docs/#oauth-2-authorize>
    MAX_RETRY_ATTEMPTS = 5


class Client(object):
    """Configuration object containing the user agent string."""
    VERSION = version.__version__
    USER_AGENT_STRING = 'box-python-sdk-{0}'.format(VERSION)
    BOX_UA_STRING = 'agent=box-python-sdk/{0}; env=python/{1}.{2}.{3}'.format(
        VERSION,
        py_version.major,
        py_version.minor,
        py_version.micro,
    )


class Proxy(object):
    URL = None
    AUTH = None
