# coding: utf-8

from __future__ import unicode_literals, absolute_import

from functools import partial
import json
from logging import Logger
from operator import attrgetter
from pprint import pformat

import mock
from mock import Mock, patch
import pytest
from six import text_type
from six.moves import map

from boxsdk.network import default_network, logging_network
from boxsdk.network.logging_network import LoggingNetwork, LoggingNetworkResponse


class ExceptionSubclass(Exception):
    pass


@pytest.fixture
def logger():
    return Mock(Logger)


@pytest.fixture
def network(logger):
    return LoggingNetwork(logger)


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
        for method_name in method_names:
            getattr(logger, method_name).assert_not_called()

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


# BEGIN Tests for LoggingNetwork.


def test_logging_network_calls_setup_logging_if_logger_is_none():
    with patch.object(logging_network, 'setup_logging') as setup_logging:
        network = LoggingNetwork()
        setup_logging.assert_called_once_with(name=LoggingNetwork.LOGGER_NAME)
        assert network.logger is setup_logging.return_value


def test_logging_network_can_be_initialized_if_logger_is_none(logger):
    with patch('logging.getLogger') as get_logger:
        get_logger.return_value = logger
        network = LoggingNetwork()
        assert network.logger is get_logger.return_value
        get_logger.assert_called_once_with(LoggingNetwork.LOGGER_NAME)


def test_logging_network_does_not_call_setup_logging_if_logger_is_not_none(logger):
    with patch.object(logging_network, 'setup_logging') as setup_logging:
        network = LoggingNetwork(logger)
        setup_logging.assert_not_called()
        assert network.logger is logger


def test_logging_network_logs_requests(make_network_request, http_verb, test_url, network, assert_logger_called_once_with):
    kwargs = dict(custom_kwarg='foo')
    make_network_request(network, **kwargs)
    assert_logger_called_once_with(
        'info',
        network.REQUEST_FORMAT,
        {'method': http_verb, 'url': test_url, 'request_kwargs': pformat(kwargs)},
    )


def test_logging_network_logs_request_exception(make_network_request, http_verb, test_url, logger, network):
    with patch.object(default_network.DefaultNetwork, 'request') as super_request:
        super_request.side_effect = expected_exception = ExceptionSubclass('exception raised from request()')
        with pytest.raises(ExceptionSubclass) as pytest_exc_info:
            make_network_request(network)
        assert pytest_exc_info.value is expected_exception
    logger.warning.assert_called_once_with(
        network.EXCEPTION_FORMAT,
        {'method': http_verb, 'url': test_url, 'exc_type_name': ExceptionSubclass.__name__, 'exc_value': expected_exception},
    )


def test_logging_network_request_returns_logging_network_response(make_network_request, request_response, network):
    response = make_network_request(network)
    assert response.request_response is request_response
    assert isinstance(response, LoggingNetworkResponse)


def test_logging_network_response_constructor(make_network_request, access_token, logger, network):
    mock_response = Mock(LoggingNetworkResponse, access_token_used=access_token)
    with patch.object(logging_network, 'LoggingNetworkResponse') as mock_logging_network_response_class:
        mock_logging_network_response_class.return_value = mock_response
        assert make_network_request(network) is mock_response
        assert mock_logging_network_response_class.call_count == 1
        kwargs = mock_logging_network_response_class.call_args[1]
        assert ('logger' in kwargs) and (kwargs['logger'] is logger)
        assert ('successful_response_format' in kwargs) and (kwargs['successful_response_format'] is network.SUCCESSFUL_RESPONSE_FORMAT)
        assert ('error_response_format' in kwargs) and (kwargs['error_response_format'] is network.ERROR_RESPONSE_FORMAT)


# END Tests for LoggingNetwork.


# BEGIN Tests for LoggingNetworkResponse.


@pytest.fixture
def construct_logging_network_response(logger, access_token):

    def _construct_logging_network_response(request_response):
        return LoggingNetworkResponse(
            logger=logger,
            successful_response_format=LoggingNetwork.SUCCESSFUL_RESPONSE_FORMAT,
            error_response_format=LoggingNetwork.ERROR_RESPONSE_FORMAT,
            request_response=request_response,
            access_token_used=access_token,
        )

    return _construct_logging_network_response


@pytest.fixture
def logging_network_response(construct_logging_network_response, request_response):
    return construct_logging_network_response(request_response)


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


def test_logging_network_response_does_not_log_anything_immediately(logging_network_response, logger_call_count):
    # pylint:disable=unused-argument
    # Need to load the `logging_network_response` fixture for this test to be
    # meaningful.
    assert logger_call_count() == 0


def test_logging_network_response_only_logs_once(logging_network_response, logger_call_count):
    logging_network_response.log()
    assert logger_call_count() == 1
    logging_network_response.log()
    assert logger_call_count() == 1


@pytest.mark.parametrize('content_length_header', [False, True])
def test_logging_network_logs_successful_responses(
        construct_logging_network_response, generic_successful_request_response, assert_logger_called_once_with,
        get_content_from_response, http_verb, test_url, content_length_header,
):
    expected_content_length = text_type(len(generic_successful_request_response.content))
    if content_length_header:
        generic_successful_request_response.headers['Content-Length'] = expected_content_length
    else:
        generic_successful_request_response.headers.pop('Content-Length', None)
    generic_successful_request_response.request.method = http_verb
    generic_successful_request_response.request.url = test_url
    logging_network_response = construct_logging_network_response(generic_successful_request_response)
    get_content_from_response(logging_network_response)
    assert_logger_called_once_with(
        'info',
        LoggingNetwork.SUCCESSFUL_RESPONSE_FORMAT,
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
def test_logging_network_logs_successful_responses_with_stream_placeholder(
        construct_logging_network_response, generic_successful_request_response, assert_logger_called_once_with,
        do_not_get_content_from_response, logger, content_length_header,
):
    if content_length_header:
        expected_content_length = text_type(len(generic_successful_request_response.content))
        generic_successful_request_response.headers['Content-Length'] = expected_content_length
    else:
        generic_successful_request_response.headers.pop('Content-Length', None)
        expected_content_length = '?'
    logging_network_response = construct_logging_network_response(generic_successful_request_response)
    do_not_get_content_from_response(logging_network_response)
    assert_logger_called_once_with('info', LoggingNetwork.SUCCESSFUL_RESPONSE_FORMAT, mock.ANY)
    assert logger.info.call_args[0][1]['content'] == logging_network_response.STREAM_CONTENT_NOT_LOGGED
    assert logger.info.call_args[0][1]['content_length'] == expected_content_length


def test_logging_network_logs_successful_responses_with_non_json_content(
        construct_logging_network_response, generic_successful_request_response, assert_logger_called_once_with,
        logger, get_content_from_response,
):
    generic_successful_request_response.content = content = (b''.join(chr(i).encode('utf-8') for i in range(128)) * 4)
    generic_successful_request_response.json.side_effect = lambda: json.loads(content.decode('utf-8'))
    logging_network_response = construct_logging_network_response(generic_successful_request_response)
    get_content_from_response(logging_network_response)
    assert_logger_called_once_with('info', LoggingNetwork.SUCCESSFUL_RESPONSE_FORMAT, mock.ANY)
    assert logger.info.call_args[0][1]['content'] == pformat(content)


def test_logging_network_logs_non_successful_responses(
        construct_logging_network_response, server_error_request_response, assert_logger_called_once_with,
        get_content_from_response, http_verb, test_url,
):
    server_error_request_response.request.method = http_verb
    server_error_request_response.request.url = test_url
    logging_network_response = construct_logging_network_response(server_error_request_response)
    get_content_from_response(logging_network_response)
    assert_logger_called_once_with(
        'warning',
        LoggingNetwork.ERROR_RESPONSE_FORMAT,
        {
            'method': http_verb,
            'url': test_url,
            'status_code': server_error_request_response.status_code,
            'content_length': text_type(len(server_error_request_response.content)),
            'headers': pformat(server_error_request_response.headers),
            'content': pformat(server_error_request_response.json()),
        }
    )


# END Tests for LoggingNetworkResponse.
