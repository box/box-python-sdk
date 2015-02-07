# coding: utf-8

from __future__ import unicode_literals

from boxsdk.config import API


def test_user_url(mock_user):
    # pylint:disable=redefined-outer-name, protected-access
    assert mock_user.get_url() == '{0}/{1}/{2}'.format(API.BASE_API_URL, 'users', mock_user.object_id)
