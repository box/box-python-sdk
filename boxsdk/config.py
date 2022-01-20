# coding: utf-8

from sys import version_info as py_version

from . import version


class API:
    """Configuration object containing the URLs for the Box API."""
    BASE_API_URL = 'https://api.box.com/2.0'
    UPLOAD_URL = 'https://upload.box.com/api/2.0'
    OAUTH2_API_URL = 'https://api.box.com/oauth2'  # <https://developers.box.com/docs/#oauth-2>
    OAUTH2_AUTHORIZE_URL = 'https://account.box.com/api/oauth2/authorize'  # <https://developers.box.com/docs/#oauth-2-authorize>
    MAX_RETRY_ATTEMPTS = 5


class Client:
    """Configuration object containing the user agent string."""
    VERSION = version.__version__
    USER_AGENT_STRING = f'box-python-sdk-{VERSION}'
    BOX_UA_STRING = f'agent=box-python-sdk/{VERSION}; ' \
                    f'env=python/{py_version.major}.{py_version.minor}.{py_version.micro}'


class Proxy:
    URL = None
    AUTH = None
