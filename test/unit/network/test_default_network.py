# coding: utf-8

from __future__ import unicode_literals
from mock import DEFAULT, Mock, patch
import pytest
from boxsdk.network.default_network import DefaultNetwork


def test_default_network_request(mock_request, http_verb, test_url, access_token, generic_successful_response):
    default_network = DefaultNetwork()
    mock_request.return_value = generic_successful_response
    response = default_network.request(http_verb, test_url, access_token, custom_kwarg='test').get()
    mock_request.assert_called_once_with(http_verb, test_url, custom_kwarg='test')
    assert response.response_as_stream == generic_successful_response.raw
    assert response.access_token_used == access_token


@pytest.mark.parametrize('delay', (0, 1))
def test_default_network_retry_after_sleeps(delay):
    default_network = DefaultNetwork()
    retry_call = Mock()
    retry_call.return_value = None
    mock_sleep = Mock()
    with patch('boxsdk.network.default_network_sync.time.sleep', mock_sleep):
        assert default_network.retry_after(delay, retry_call, DEFAULT, kwarg=DEFAULT).get() is None
    mock_sleep.assert_called_once_with(delay)
    retry_call.assert_called_once_with(DEFAULT, kwarg=DEFAULT)
