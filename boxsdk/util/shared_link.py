# coding: utf-8

from __future__ import unicode_literals


def get_shared_link_header(shared_link, password=None):
    """
    Gets the HTTP header required to use a shared link to grant access to a shared item.

    :param shared_link:
        The shared link.
    :type shared_link:
        `unicode`
    :param password:
        The password for the shared link.
    :type password:
        `unicode`
    :return:
        The item referred to by the shared link.
    :rtype:
        :class:`Item`
    """
    shared_link_password = '&shared_link_password={0}'.format(password) if password is not None else ''
    box_api_header = 'shared_link={0}{1}'.format(shared_link, shared_link_password)
    return {'BoxApi': box_api_header}
