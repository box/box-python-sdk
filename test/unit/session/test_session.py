# coding: utf-8

from functools import partial
from io import IOBase
from numbers import Number

from mock import MagicMock, Mock, PropertyMock, call, patch, ANY
import pytest

from boxsdk.auth.oauth2 import OAuth2
from boxsdk.config import API, Proxy
from boxsdk.exception import BoxAPIException, BoxException
from boxsdk.network.default_network import DefaultNetwork, DefaultNetworkResponse
from boxsdk.session.box_response import BoxResponse
from boxsdk.session.session import Session, Translator, AuthorizedSession


@pytest.fixture(scope='function', params=[False, True])
def translator(default_translator, request):  # pylint:disable=unused-argument
    if request.param:
        return Translator(extend_default_translator=True, new_child=True)
    return None


@pytest.fixture
def initial_access_token():
    return 'fake_access_token'


@pytest.fixture
def mock_oauth(initial_access_token):
    mock_oauth = MagicMock(OAuth2)
    mock_oauth.access_token = initial_access_token
    return mock_oauth


@pytest.fixture
def mock_network_layer():
    return Mock(DefaultNetwork)


@pytest.fixture
def unauthorized_session(mock_network_layer, translator):
    # pylint:disable=redefined-outer-name
    return Session(network_layer=mock_network_layer, translator=translator)


@pytest.fixture
def box_session(mock_oauth, mock_network_layer, translator):
    # pylint:disable=redefined-outer-name
    return AuthorizedSession(oauth=mock_oauth, network_layer=mock_network_layer, translator=translator)


@pytest.mark.parametrize('test_method', [
    Session.get,
    Session.post,
    Session.put,
    Session.delete,
    Session.options,
])
def test_box_session_handles_unauthorized_response(
        test_method,
        box_session,
        mock_oauth,
        mock_network_layer,
        unauthorized_response,
        generic_successful_response,
        test_url,
):
    # pylint:disable=redefined-outer-name

    def get_access_token_from_auth_object():
        return mock_oauth.access_token

    mock_network_layer.request.side_effect = mock_responses = [unauthorized_response, generic_successful_response]
    for mock_response in mock_responses:
        type(mock_response).access_token_used = PropertyMock(side_effect=get_access_token_from_auth_object)

    def refresh(access_token_used):
        assert access_token_used == mock_oauth.access_token
        mock_oauth.access_token = 'fake_new_access_token'
        return (mock_oauth.access_token, None)

    mock_oauth.refresh.side_effect = refresh

    box_response = test_method(box_session, url=test_url)
    assert box_response.status_code == 200


@pytest.mark.parametrize('test_method', [
    Session.get,
    Session.post,
    Session.put,
    Session.delete,
    Session.options,
])
@pytest.mark.parametrize('initial_access_token', [None])
def test_box_session_gets_access_token_before_request(
        test_method,
        box_session,
        mock_oauth,
        mock_network_layer,
        generic_successful_response,
        test_url,
):
    # pylint:disable=redefined-outer-name

    def get_access_token_from_auth_object():
        return mock_oauth.access_token

    mock_network_layer.request.side_effect = mock_responses = [generic_successful_response]
    for mock_response in mock_responses:
        type(mock_response).access_token_used = PropertyMock(side_effect=get_access_token_from_auth_object)

    def refresh(access_token_used):
        assert access_token_used == mock_oauth.access_token
        mock_oauth.access_token = 'fake_new_access_token'
        return (mock_oauth.access_token, None)

    mock_oauth.refresh.side_effect = refresh

    box_response = test_method(box_session, url=test_url, auto_session_renewal=True)
    assert box_response.status_code == 200


@pytest.mark.parametrize('test_method', [
    Session.get,
    Session.post,
    Session.put,
    Session.delete,
    Session.options,
    partial(Session.request, method='head'),
])
def test_box_session_retries_response_after_retry_after(
        test_method,
        box_session,
        mock_network_layer,
        retry_after_response,
        generic_successful_response,
        test_url,
):
    # pylint:disable=redefined-outer-name
    mock_network_layer.request.side_effect = [retry_after_response, generic_successful_response]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)

    with patch('random.uniform', return_value=0.68):
        box_response = test_method(box_session, url=test_url)
    assert box_response.status_code == 200
    assert len(mock_network_layer.retry_after.call_args_list) == 1
    assert isinstance(mock_network_layer.retry_after.call_args[0][0], Number)
    assert round(mock_network_layer.retry_after.call_args[0][0], 4) == 1


@pytest.mark.parametrize('test_method', [
    Session.get,
    Session.post,
    Session.put,
    Session.delete,
    Session.options,
    partial(Session.request, method='head'),
])
def test_box_session_retries_request_after_server_error(
        test_method,
        box_session,
        mock_network_layer,
        server_error_response,
        generic_successful_response,
        test_url,
):
    # pylint:disable=redefined-outer-name
    mock_network_layer.request.side_effect = [server_error_response, server_error_response, generic_successful_response]
    mock_network_layer.retry_after.side_effect = lambda delay, request, *args, **kwargs: request(*args, **kwargs)

    with patch('random.uniform', return_value=0.68):
        box_response = test_method(box_session, url=test_url)
    assert box_response.status_code == 200
    assert box_response.json() == generic_successful_response.json()
    assert box_response.ok == generic_successful_response.ok
    assert box_response.content == generic_successful_response.content
    assert len(mock_network_layer.retry_after.call_args_list) == 2
    assert isinstance(mock_network_layer.retry_after.call_args_list[0][0][0], Number)
    assert isinstance(mock_network_layer.retry_after.call_args_list[1][0][0], Number)
    assert round(mock_network_layer.retry_after.call_args_list[0][0][0], 4) == 1.18
    assert round(mock_network_layer.retry_after.call_args_list[1][0][0], 4) == 2.36


def test_box_session_seeks_file_after_retry(box_session, mock_network_layer, server_error_response, generic_successful_response, test_url):
    # pylint:disable=redefined-outer-name
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


def test_box_session_raises_for_non_json_response(box_session, mock_network_layer, non_json_response, test_url):
    # pylint:disable=redefined-outer-name
    mock_network_layer.request.side_effect = [non_json_response]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url)


def test_box_session_raises_for_failed_response(box_session, mock_network_layer, bad_network_response, test_url):
    # pylint:disable=redefined-outer-name
    mock_network_layer.request.side_effect = [bad_network_response]

    with pytest.raises(BoxAPIException):
        box_session.get(url=test_url)


def test_box_session_raises_for_failed_response_with_error_and_error_description(box_session, mock_network_layer, bad_network_response_400, test_url):
    mock_network_layer.request.side_effect = [bad_network_response_400]
    try:
        box_session.get(url=test_url)
        pytest.fail('Should throw exception because of bad network response')
    except BoxAPIException as exception:
        assert exception.code == 'Example Error'
        assert exception.message == 'Example Error Description'


def test_box_session_raises_for_failed_non_json_response(box_session, mock_network_layer, failed_non_json_response, test_url):
    # pylint:disable=redefined-outer-name
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


def test_translator(box_session, translator, default_translator, original_default_translator):
    assert isinstance(box_session.translator, Translator)
    assert box_session.translator == default_translator
    if translator:
        assert box_session.translator is translator

    # Test that adding new registrations works.

    class Foo:
        pass

    item_type = u'ƒøø'
    box_session.translator.register(item_type, Foo)
    assert box_session.translator.get(item_type) is Foo

    # Test that adding new registrations does not affect global state.
    assert default_translator == original_default_translator
    assert (set(box_session.translator) - set(default_translator)) == set([item_type])


def test_session_uses_global_config(box_session, mock_network_layer, generic_successful_response, monkeypatch):
    mock_network_layer.request.side_effect = generic_successful_response
    example_dot_com = 'https://example.com/'
    monkeypatch.setattr(API, 'BASE_API_URL', example_dot_com)
    assert example_dot_com in box_session.get_url('foo', 'bar')


def test_session_uses_local_config(box_session, mock_network_layer, generic_successful_response, monkeypatch):
    mock_network_layer.request.side_effect = generic_successful_response
    example_dot_com = 'https://example.com/'
    box_session.api_config.BASE_API_URL = example_dot_com
    monkeypatch.setattr(API, 'BASE_API_URL', 'https://api.box.com')
    assert example_dot_com in box_session.get_url('foo', 'bar')


@pytest.mark.parametrize(
    'attempt_number,retry_after_header,expected_result',
    [
        (0, '', 1.18),
        (1, '', 2.36),
        (2, '', 4.72),
        (3, '', 9.44),
        (4, '', 18.88),
    ]
)
def test_get_retry_after_time(box_session, attempt_number, retry_after_header, expected_result):
    with patch('random.uniform', return_value=0.68):
        retry_time = box_session.get_retry_after_time(attempt_number, retry_after_header)  # pylint: disable=protected-access
    retry_time = round(retry_time, 4)
    assert retry_time == expected_result


@pytest.mark.parametrize(
    'test_proxy_url,test_proxy_auth,expected_proxy_dict',
    [
        ('http://example-proxy.com', {'user': 'test_user', 'password': 'test_password', },
         {'http': 'http://test_user:test_password@example-proxy.com', 'https': 'http://test_user:test_password@example-proxy.com'}),
        ('http://example-proxy.com', None, {'http': 'http://example-proxy.com', 'https': 'http://example-proxy.com'}),
    ]
)
def test_proxy_attaches_to_request_correctly(
        box_session,
        monkeypatch,
        mock_network_layer,
        generic_successful_response,
        test_proxy_url, test_proxy_auth,
        expected_proxy_dict):
    monkeypatch.setattr(Proxy, 'URL', test_proxy_url)
    monkeypatch.setattr(Proxy, 'AUTH', test_proxy_auth)
    mock_network_layer.request.side_effect = [generic_successful_response]
    box_session.request('GET', test_proxy_url)
    mock_network_layer.request.assert_called_once_with(
        'GET',
        test_proxy_url,
        access_token='fake_access_token',
        headers=ANY,
        proxies=expected_proxy_dict,
    )


def test_proxy_malformed_dict_does_not_attach(box_session, monkeypatch, mock_network_layer, generic_successful_response):
    test_proxy_url = 'http://example.com'
    test_proxy_auth = {
        'foo': 'bar',
    }
    monkeypatch.setattr(Proxy, 'URL', test_proxy_url)
    monkeypatch.setattr(Proxy, 'AUTH', test_proxy_auth)
    mock_network_layer.request.side_effect = [generic_successful_response]
    with pytest.raises(BoxException) as exc_info:
        box_session.request('GET', test_proxy_url)
    assert isinstance(exc_info.value, BoxException)
    assert exc_info.value.args[0] == "The proxy auth dict you provided does not match pattern " \
                                     "{'user': 'example_user', 'password': 'example_password'}"


def test_proxy_network_config_property(box_session):
    assert isinstance(box_session.proxy_config, Proxy)
