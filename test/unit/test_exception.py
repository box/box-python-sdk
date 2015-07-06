# coding: utf-8

from __future__ import unicode_literals
from boxsdk.exception import BoxAPIException, BoxOAuthException


def test_box_api_exception():
    status = 'status'
    code = 400
    message = 'message'
    request_id = 12345
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
    assert box_exception._headers == headers  # pylint:disable=protected-access
    assert box_exception.url == url
    assert box_exception.method == method
    assert box_exception.context_info == context_info
    assert str(box_exception) == '''
Message: {0}
Status: {1}
Code: {2}
Request id: {3}
Headers: {4}
URL: {5}
Method: {6}
Context info: {7}'''.format(message, status, code, request_id, headers, url, method, context_info)


def test_box_oauth_exception():
    status = 'status'
    message = 'message'
    url = 'https://example.com'
    method = 'GET'
    box_exception = BoxOAuthException(
        status,
        message=message,
        url=url,
        method=method,
    )
    assert str(box_exception) == '''
Message: {0}
Status: {1}
URL: {2}
Method: {3}'''.format(message, status, url, method)
