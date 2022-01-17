# coding: utf-8

from mock import Mock
import pytest

from boxsdk.exception import BoxAPIException, BoxOAuthException
from boxsdk.network.default_network import DefaultNetworkResponse


def test_box_api_exception():
    status = 400
    code = 'code'
    message = 'message'
    request_id = '12345'
    headers = {'header': 'value'}
    url = 'https://example.com'
    method = 'GET'
    context_info = {'context': 'value'}
    box_exception = BoxAPIException(
        status,
        code=code,
        message=message,
        request_id=request_id,
        headers=headers,
        url=url,
        method=method,
        context_info=context_info,
    )
    assert box_exception.status == status
    assert box_exception.code == code
    assert box_exception.message == message
    assert box_exception.request_id == request_id
    assert box_exception.headers == headers  # pylint:disable=protected-access
    assert box_exception.url == url
    assert box_exception.method == method
    assert box_exception.context_info == context_info
    assert str(box_exception) == f'''Message: {message}
Status: {status}
Code: {code}
Request ID: {request_id}
Headers: {headers}
URL: {url}
Method: {method}
Context Info: {context_info}'''


@pytest.mark.parametrize('has_network_response', [True, False])
def test_box_oauth_exception(has_network_response):
    status = 400
    message = 'message'
    url = 'https://example.com'
    method = 'GET'
    headers = {'header': 'value'}
    network_response = Mock(DefaultNetworkResponse, headers=headers) if has_network_response else None
    box_exception = BoxOAuthException(
        status,
        message=message,
        url=url,
        method=method,
        network_response=network_response,
    )
    assert str(box_exception) == f'''
Message: {message}
Status: {status}
URL: {url}
Method: {method}
Headers: {headers if has_network_response else 'N/A'}'''
    assert box_exception.network_response is network_response
