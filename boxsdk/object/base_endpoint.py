# coding: utf-8

from __future__ import unicode_literals
from boxsdk.config import API


class BaseEndpoint(object):
    """A Box API endpoint."""

    def __init__(self, session):
        """

        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        """
        self._session = session

    def get_url(self, endpoint, *args):
        """
        Return the URL used to access the endpoint.

        :param endpoint:
            The name of the endpoint.
        :type endpoint:
            `url`
        :param args:
            Additional parts of the endpoint URL.
        :type args:
            `Iterable`
        :rtype:
            `unicode`
        """
        # pylint:disable=no-self-use
        url = ['{0}/{1}'.format(API.BASE_API_URL, endpoint)]
        url.extend(['/{0}'.format(x) for x in args])
        return ''.join(url)
