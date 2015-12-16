# coding: utf-8

from __future__ import unicode_literals

from functools import partial
from io import IOBase
from numbers import Number

from mock import MagicMock, Mock, call
import pytest

from boxsdk.auth.oauth2 import OAuth2
from boxsdk.exception import BoxAPIException
from boxsdk.network.default_network import DefaultNetwork, DefaultNetworkResponse
from boxsdk.session.box_session import BoxSession, BoxResponse


@pytest.fixture
def box_session():
    mock_oauth = Mock(OAuth2)
    mock_oauth.access_token = 'fake_access_token'

    mock_network_layer = Mock(DefaultNetwork)

    return BoxSession(mock_oauth, mock_network_layer)


@pytest.mark.parametrize('test_method', [
    BoxSession.get,
    BoxSession.post,
    BoxSession.put,
    BoxSession.delete,
    BoxSession.options,
])
def test_box_session_handles_unauthorized_response(
        test_method,
        box_session,
        unauthorized_response,
        generic_successful_response,
        test_url,
):
    # pylint:disable=redefined-outer-name, protected-access
    mock_network_layer = box_session._network_layer
    mock_network_layer.request.side_effect = [unauthorized_response, generic_successful_response]

    box_response = test_method(box_session, url=test_url)
    assert box_response.status_code == 200


@pytest.mark.parametrize('test_method', [
    BoxSession.get,
    BoxSession.post,
    BoxSession.put,
    BoxSession.delete,
    BoxSession.options,
    partial(BoxSession.request, method='head'),
])
def test_box_session_retries_response_after_retry_after(
        test_method,
        box_session,
        retry_after_response,
        generic_successful_response,
        test_url,
):
    # pylint:disable=redefined-outer-name, protected-access
    mock_network_layer = box_session._network_layer
    mock_network_layer.request.side_effect = [retry_after_response, generic_successful_response]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)

    box_response = test_method(box_session, url=test_url)
    assert box_response.status_code == 200
    assert len(mock_network_layer.retry_after.call_args_list) == 1
    assert isinstance(mock_network_layer.retry_after.call_args[0][0], Number)
    assert mock_network_layer.retry_after.call_args[0][0] == float(retry_after_response.headers['Retry-After'])


@pytest.mark.parametrize('test_method', [
    BoxSession.get,
    BoxSession.post,
    BoxSession.put,
    BoxSession.delete,
    BoxSession.options,
    partial(BoxSession.request, method='head'),
])
def test_box_session_retries_request_after_server_error(
        test_method,
        box_session,
        server_error_response,
        generic_successful_response,
        test_url,
):
    # pylint:disable=redefined-outer-name, protected-access
    mock_network_layer = box_session._network_layer
    mock_network_layer.request.side_effect = [server_error_response, server_error_response, generic_successful_response]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)

    box_response = test_method(box_session, url=test_url)
    assert box_response.status_code == 200
    assert box_response.json() == generic_successful_response.json()
    assert box_response.ok == generic_successful_response.ok
    assert box_response.content == generic_successful_response.content
    assert len(mock_network_layer.retry_after.call_args_list) == 2
    assert isinstance(mock_network_layer.retry_after.call_args_list[0][0][0], Number)
    assert isinstance(mock_network_layer.retry_after.call_args_list[1][0][0], Number)
    assert mock_network_layer.retry_after.call_args_list[0][0][0] == 1
    assert mock_network_layer.retry_after.call_args_list[1][0][0] == 2


def test_box_session_seeks_file_after_retry(box_session, server_error_response, generic_successful_response, test_url):
    # pylint:disable=redefined-outer-name, protected-access
    mock_network_layer = box_session._network_layer
    mock_network_layer.request.side_effect = [server_error_response, generic_successful_response]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)
    mock_file_1, mock_file_2 = MagicMock(IOBase), MagicMock(IOBase)
    mock_file_1.tell.return_value = 0
    mock_file_2.tell.return_value = 3
    files = {'file': ('unused', mock_file_1), 'f2': ('unused', mock_file_2)}

    box_response = box_session.post(url=test_url, files=files)
    assert box_response.status_code == 200
    assert box_response.json() == generic_successful_response.json()
    assert box_response.ok == generic_successful_response.ok
    mock_file_1.tell.assert_called_with()
    mock_file_2.tell.assert_called_with()
    mock_file_1.seek.assert_called_with(0)
    assert mock_file_1.seek.call_count == 2
    assert mock_file_1.seek.has_calls(call(0) * 2)
    mock_file_2.seek.assert_called_with(3)
    assert mock_file_2.seek.call_count == 2
    assert mock_file_2.seek.has_calls(call(3) * 2)


def test_box_session_raises_for_non_json_response(box_session, non_json_response, test_url):
    # pylint:disable=redefined-outer-name, protected-access
    mock_network_layer = box_session._network_layer
    mock_network_layer.request.side_effect = [non_json_response]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url)


def test_box_session_raises_for_failed_response(box_session, bad_network_response, test_url):
    # pylint:disable=redefined-outer-name, protected-access
    mock_network_layer = box_session._network_layer
    mock_network_layer.request.side_effect = [bad_network_response]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url)


def test_box_session_raises_for_failed_non_json_response(box_session, failed_non_json_response, test_url):
    # pylint:disable=redefined-outer-name, protected-access
    mock_network_layer = box_session._network_layer
    mock_network_layer.request.side_effect = [failed_non_json_response]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url, expect_json_response=False)


def test_box_response_properties_pass_through_to_network_response_properties():
    mock_network_response = Mock(DefaultNetworkResponse)
    box_result = BoxResponse(mock_network_response)
    assert box_result.json() == mock_network_response.json()
    assert box_result.content == mock_network_response.content
    assert box_result.ok == mock_network_response.ok
    assert box_result.status_code == mock_network_response.status_code
    assert box_result.network_response == mock_network_response
