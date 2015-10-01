# coding: utf-8

from __future__ import unicode_literals
from mock import ANY, call
from boxsdk.config import API


def test_automatic_refresh(
        box_client,
        mock_box_network,
        generic_successful_response,
        successful_token_response,
        unauthorized_response,
):
    mock_box_network.session.request.side_effect = [
        unauthorized_response,
        successful_token_response,
        generic_successful_response,
    ]
    box_client.folder('0').get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            '{0}/folders/0'.format(API.BASE_API_URL),
            headers=ANY,
            params=None,
        ),
        call(
            'POST',
            '{0}/token'.format(API.OAUTH2_API_URL),
            data=ANY,
            headers={'content-type': 'application/x-www-form-urlencoded'},
        ),
        call(
            'GET',
            '{0}/folders/0'.format(API.BASE_API_URL),
            headers=ANY,
            params=None,
        ),
    ]
