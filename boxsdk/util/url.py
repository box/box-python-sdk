# coding: utf-8

from __future__ import unicode_literals, absolute_import

from boxsdk.config import API


def get_url(endpoint, *args):
    """
    Return the URL for the given Box API endpoint.

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
    url = ['{0}/{1}'.format(API.BASE_API_URL, endpoint)]
    url.extend(['/{0}'.format(x) for x in args])
    return ''.join(url)
