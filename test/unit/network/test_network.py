# coding: utf-8

from functools import partial
import json
from logging import Logger
from operator import attrgetter
from pprint import pformat

from mock import DEFAULT, Mock, patch, ANY
import pytest
from requests import Response

from boxsdk.network import default_network
from boxsdk.network.default_network import DefaultNetworkResponse, DefaultNetwork


class ExceptionSubclass(Exception):
    pass


@pytest.fixture
def logger():
    return Mock(Logger)


@pytest.fixture
def network():
    return DefaultNetwork()


@pytest.fixture(autouse=True)
def mocked_logger(logger):
    with patch.object(default_network, 'getLogger') as get_logger:
        get_logger.return_value = logger
        yield


@pytest.fixture(scope='module')
def logger_method_names():
    return ['critical', 'debug', 'error', 'exception', 'fatal', 'info', 'log', 'warn', 'warning']


@pytest.fixture
def logger_methods(logger, logger_method_names):
    return list(map(partial(getattr, logger), logger_method_names))


@pytest.fixture
def assert_logger_called_once_with(logger, logger_method_names):

    def _assert_logger_called_once_with(method_name, *args, **kwargs):
        getattr(logger, method_name).assert_called_once_with(*args, **kwargs)
        method_names = set(logger_method_names)
        method_names.discard(method_name)
        for name in method_names:
            getattr(logger, name).assert_not_called()

    return _assert_logger_called_once_with


@pytest.fixture
def assert_logger_not_called(logger_methods):

    def _assert_logger_not_called():
        for method in logger_methods:
            method.assert_not_called()

    return _assert_logger_not_called


@pytest.fixture
def logger_call_count(logger_methods):

    def _logger_call_count():
        return sum(map(attrgetter('call_count'), logger_methods))

    return _logger_call_count


@pytest.fixture
def make_network_request_and_assert_response(make_network_request, request_response):
    # pylint:disable=unused-argument

    def _make_network_request(*args, **kwargs):
        response = make_network_request(*args, **kwargs)
        assert response.request_response is request_response
        return response

    return _make_network_request


@pytest.fixture
def construct_network_response(access_token):

    def _construct_network_response(request_response):
        return DefaultNetworkResponse(
            request_response=request_response,
            access_token_used=access_token,
        )

    return _construct_network_response


@pytest.fixture
def network_response(construct_network_response, request_response):
    return construct_network_response(request_response)


@pytest.fixture(params=['content', 'json'])
def get_content_from_response(request):

    def _get_content_from_response(response):
        content = getattr(response, request.param)
        if request.param in ['json']:
            try:
                content = content()
            except ValueError:
                pass

    return _get_content_from_response


@pytest.fixture(params=['response_as_stream', 'request_response', 'log'])
def do_not_get_content_from_response(request):

    def _do_not_get_content_from_response(response):
        attribute = getattr(response, request.param)
        if request.param in ['log']:
            attribute()

    return _do_not_get_content_from_response


# BEGIN Tests for DefaultNetwork.


def test_default_network_response_properties_pass_through_to_session_response_properties(access_token):
    mock_session_response = Mock(Response)
    mock_session_response.status_code = 200
    mock_session_response.headers = {}
    mock_session_response.raw = Mock()
    mock_session_response.content = json.dumps('content')
    mock_session_response.request = Mock()
    network_reponse = DefaultNetworkResponse(mock_session_response, access_token)
    assert network_reponse.json() == mock_session_response.json()
    assert network_reponse.content == mock_session_response.content
    assert network_reponse.ok == mock_session_response.ok
    assert network_reponse.status_code == mock_session_response.status_code
    assert network_reponse.headers == mock_session_response.headers
    assert network_reponse.response_as_stream == mock_session_response.raw
    assert network_reponse.access_token_used == access_token


def test_default_network_request(make_network_request_and_assert_response):
    # pylint:disable=redefined-outer-name
    default_network = DefaultNetwork()
    make_network_request_and_assert_response(default_network, custom_kwargs='test')


@pytest.mark.parametrize('delay', (0, 1))
def test_default_network_retry_after_sleeps(delay):
    default_network = DefaultNetwork()
    retry_call = Mock()
    mock_sleep = Mock()
    with patch('boxsdk.network.default_network.time.sleep', mock_sleep):
        default_network.retry_after(delay, retry_call, DEFAULT, kwarg=DEFAULT)
    mock_sleep.assert_called_once_with(delay)
    retry_call.assert_called_once_with(DEFAULT, kwarg=DEFAULT)


def test_network_response_constructor(make_network_request_and_assert_response):
    assert DefaultNetwork().network_response_constructor is DefaultNetworkResponse

    class DefaultNetworkResponseSubclass(DefaultNetworkResponse):
        pass

    class DefaultNetworkSubclass(DefaultNetwork):
        @property
        def network_response_constructor(self):
            return DefaultNetworkResponseSubclass

    network = DefaultNetworkSubclass()
    response = make_network_request_and_assert_response(network)
    assert isinstance(response, DefaultNetworkResponseSubclass)


def test_network_logs_requests(make_network_request, http_verb, test_url, network, logger):
    kwargs = dict(custom_kwarg='foo')
    make_network_request(network, **kwargs)
    logger.info.assert_called_once_with(
        network.REQUEST_FORMAT,
        {'method': http_verb, 'url': test_url, 'request_kwargs': pformat(kwargs)},
    )


def test_network_logs_request_exception(make_network_request, mock_request, http_verb, test_url, logger, network):
    mock_request.side_effect = expected_exception = ExceptionSubclass('exception raised from request()')
    with pytest.raises(ExceptionSubclass) as pytest_exc_info:
        make_network_request(network)
    assert pytest_exc_info.value is expected_exception
    logger.warning.assert_called_once_with(
        network.EXCEPTION_FORMAT,
        {'method': http_verb, 'url': test_url, 'exc_type_name': ExceptionSubclass.__name__, 'exc_value': expected_exception},
    )


def test_network_request_returns_network_response(make_network_request, request_response, network):
    response = make_network_request(network)
    assert response.request_response is request_response
    assert isinstance(response, DefaultNetworkResponse)


# BEGIN Tests for NetworkResponse.


def test_error_network_response_logs_immediately(network_response, logger_call_count):
    # pylint:disable=unused-argument
    # Need to load the `network_response` fixture for this test to be
    # meaningful.
    assert logger_call_count() == 0 if network_response.ok else 1


def test_network_response_only_logs_once(network_response, logger_call_count):
    network_response.log()
    assert logger_call_count() == 1
    network_response.log()
    assert logger_call_count() == 1


@pytest.mark.parametrize('content_length_header', [False, True])
def test_network_logs_successful_responses(
        construct_network_response, generic_successful_request_response, assert_logger_called_once_with,
        get_content_from_response, http_verb, test_url, content_length_header,
):
    expected_content_length = str(len(generic_successful_request_response.content))
    if content_length_header:
        generic_successful_request_response.headers['Content-Length'] = expected_content_length
    else:
        generic_successful_request_response.headers.pop('Content-Length', None)
    generic_successful_request_response.request.method = http_verb
    generic_successful_request_response.request.url = test_url
    network_response = construct_network_response(generic_successful_request_response)
    get_content_from_response(network_response)
    assert_logger_called_once_with(
        'info',
        DefaultNetworkResponse.SUCCESSFUL_RESPONSE_FORMAT,
        {
            'method': http_verb,
            'url': test_url,
            'status_code': generic_successful_request_response.status_code,
            'content_length': expected_content_length,
            'headers': pformat(generic_successful_request_response.headers),
            'content': pformat(generic_successful_request_response.json()),
        }
    )


@pytest.mark.parametrize('content_length_header', [False, True])
def test_network_logs_successful_responses_with_stream_placeholder(
        construct_network_response, generic_successful_request_response, assert_logger_called_once_with,
        do_not_get_content_from_response, logger, content_length_header,
):
    if content_length_header:
        expected_content_length = str(len(generic_successful_request_response.content))
        generic_successful_request_response.headers['Content-Length'] = expected_content_length
    else:
        generic_successful_request_response.headers.pop('Content-Length', None)
        expected_content_length = '?'
    network_response = construct_network_response(generic_successful_request_response)
    do_not_get_content_from_response(network_response)
    assert_logger_called_once_with('info', DefaultNetworkResponse.SUCCESSFUL_RESPONSE_FORMAT, ANY)
    assert logger.info.call_args[0][1]['content'] == network_response.STREAM_CONTENT_NOT_LOGGED
    assert logger.info.call_args[0][1]['content_length'] == expected_content_length


def test_network_logs_successful_responses_with_non_json_content(
        construct_network_response, generic_successful_request_response, assert_logger_called_once_with,
        logger, get_content_from_response,
):
    generic_successful_request_response.content = content = (b''.join(chr(i).encode('utf-8') for i in range(128)) * 4)
    generic_successful_request_response.json.side_effect = lambda: json.loads(content.decode('utf-8'))
    network_response = construct_network_response(generic_successful_request_response)
    get_content_from_response(network_response)
    assert_logger_called_once_with('info', DefaultNetworkResponse.SUCCESSFUL_RESPONSE_FORMAT, ANY)
    assert logger.info.call_args[0][1]['content'] == pformat(content)


def test_network_logs_non_successful_responses(
        construct_network_response, server_error_request_response, assert_logger_called_once_with,
        http_verb, test_url,
):
    server_error_request_response.request.method = http_verb
    server_error_request_response.request.url = test_url
    construct_network_response(server_error_request_response)
    assert_logger_called_once_with(
        'warning',
        DefaultNetworkResponse.ERROR_RESPONSE_FORMAT,
        {
            'method': http_verb,
            'url': test_url,
            'status_code': server_error_request_response.status_code,
            'content_length': str(len(server_error_request_response.content)),
            'headers': pformat(server_error_request_response.headers),
            'content': pformat(server_error_request_response.json()),
        }
    )


# END Tests for NetworkResponse.
