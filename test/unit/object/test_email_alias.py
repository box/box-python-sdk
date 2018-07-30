# coding: utf-8

# from __future__ import unicode_literals
# import json

# from mock import Mock
# import pytest
# from boxsdk.config import API


# def test_delete(test_email_alias, mock_box_session):
#     expected_url = '{0}/users/{1}/email_aliases'.format(API.BASE_API_URL, mock_user.object_id)
#     test_email_alias.delete()
#     mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
