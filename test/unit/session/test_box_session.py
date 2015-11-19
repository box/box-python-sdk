# coding: utf-8

from __future__ import unicode_literals

from aplus import Promise
from functools import partial
from io import IOBase
from mock import MagicMock, Mock, call
from numbers import Number
import pytest

from boxsdk.auth.oauth2 import OAuth2
from boxsdk.exception import BoxAPIException
from boxsdk.network.default_network import DefaultNetwork
from boxsdk.network.network_interface import NetworkResponse
from boxsdk.session.box_session import BoxSession, BoxResponse


@pytest.fixture
def mock_network_layer():
    return Mock(DefaultNetwork)


@pytest.fixture
def box_session(mock_network_layer):
    mock_oauth = Mock(OAuth2)
    mock_oauth.access_token = 'fake_access_token'
    return BoxSession(mock_oauth, mock_network_layer)


@pytest.fixture(params=(
    BoxSession.get,
    BoxSession.post,
    BoxSession.put,
    BoxSession.delete,
    BoxSession.options,
    partial(BoxSession.request, method='head')
))
def test_method(request):
    return request.param


def test_box_session_handles_unauthorized_response(
        test_method,
        box_session,
        unauthorized_response,
        generic_successful_response,
        test_url,
        mock_network_layer,
):
    mock_network_layer.request.side_effect = [
        Promise.fulfilled(unauthorized_response),
        Promise.fulfilled(generic_successful_response),
    ]

    box_response = test_method(box_session, url=test_url).get()
    assert box_response.status_code == 200


def test_box_session_retries_response_after_retry_after(
        test_method,
        box_session,
        retry_after_response,
        generic_successful_response,
        test_url,
        mock_network_layer,
):
    mock_network_layer.request.side_effect = [
        Promise.fulfilled(retry_after_response),
        Promise.fulfilled(generic_successful_response),
    ]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)

    box_response = test_method(box_session, url=test_url).get()
    assert box_response.status_code == 200
    assert len(mock_network_layer.retry_after.call_args_list) == 1
    assert isinstance(mock_network_layer.retry_after.call_args[0][0], Number)
    assert mock_network_layer.retry_after.call_args[0][0] == float(retry_after_response.headers['Retry-After'])


def test_box_session_retries_request_after_server_error(
        test_method,
        box_session,
        server_error_response,
        generic_successful_response,
        test_url,
        mock_network_layer,
):
    mock_network_layer.request.side_effect = [
        Promise.fulfilled(server_error_response),
        Promise.fulfilled(server_error_response),
        Promise.fulfilled(generic_successful_response),
    ]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)

    box_response = test_method(box_session, url=test_url).get()
    assert box_response.status_code == 200
    assert box_response.json() == generic_successful_response.json()
    assert box_response.ok == generic_successful_response.ok
    assert box_response.content == generic_successful_response.content
    assert len(mock_network_layer.retry_after.call_args_list) == 2
    assert isinstance(mock_network_layer.retry_after.call_args_list[0][0][0], Number)
    assert isinstance(mock_network_layer.retry_after.call_args_list[1][0][0], Number)
    assert mock_network_layer.retry_after.call_args_list[0][0][0] == 1
    assert mock_network_layer.retry_after.call_args_list[1][0][0] == 2


def test_box_session_seeks_file_after_retry(
        box_session,
        server_error_response,
        generic_successful_response,
        test_url,
        mock_network_layer,
):
    mock_network_layer.request.side_effect = [
        Promise.fulfilled(server_error_response),
        Promise.fulfilled(generic_successful_response),
    ]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)
    mock_file_1, mock_file_2 = MagicMock(IOBase), MagicMock(IOBase)
    mock_file_1.tell.return_value = 0
    mock_file_2.tell.return_value = 3
    files = {'file': ('unused', mock_file_1), 'f2': ('unused', mock_file_2)}

    box_response = box_session.post(url=test_url, files=files).get()
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


def test_box_session_raises_for_non_json_response(box_session, non_json_response, test_url, mock_network_layer):
    mock_network_layer.request.side_effect = [Promise.fulfilled(non_json_response)]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url).get()


def test_box_session_raises_for_failed_response(box_session, bad_network_response, test_url, mock_network_layer):
    mock_network_layer.request.side_effect = [Promise.fulfilled(bad_network_response)]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url).get()


def test_box_session_raises_for_failed_non_json_response(
        box_session,
        failed_non_json_response,
        test_url,
        mock_network_layer,
):
    mock_network_layer.request.side_effect = [Promise.fulfilled(failed_non_json_response)]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url, expect_json_response=False).get()


def test_box_response_properties_pass_through_to_network_response_properties():
    mock_network_response = Mock(NetworkResponse)
    box_result = BoxResponse(mock_network_response)
    assert box_result.json() == mock_network_response.json()
    assert box_result.content == mock_network_response.content
    assert box_result.ok == mock_network_response.ok
    assert box_result.status_code == mock_network_response.status_code
    assert box_result.network_response == mock_network_response
