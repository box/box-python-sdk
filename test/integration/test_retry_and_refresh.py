# coding: utf-8

from mock import ANY, call
from boxsdk.config import API


def test_automatic_refresh(
        box_client,
        mock_box_network,
        generic_successful_response,
        successful_token_mock,
        unauthorized_response,
):
    mock_box_network.session.request.side_effect = [
        unauthorized_response,
        successful_token_mock,
        generic_successful_response,
    ]
    box_client.folder('0').get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            f'{API.BASE_API_URL}/folders/0',
            headers=ANY,
            params=None,
        ),
        call(
            'POST',
            f'{API.OAUTH2_API_URL}/token',
            data=ANY,
            headers={'content-type': 'application/x-www-form-urlencoded', 'User-Agent': ANY, 'X-Box-UA': ANY},
        ),
        call(
            'GET',
            f'{API.BASE_API_URL}/folders/0',
            headers=ANY,
            params=None,
        ),
    ]
