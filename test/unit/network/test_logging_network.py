# coding: utf-8

from __future__ import unicode_literals, absolute_import

from logging import Logger
from mock import Mock, patch

from boxsdk.network import default_network, logging_network
from boxsdk.network.logging_network import LoggingNetwork


def test_logging_network_calls_setup_logging_if_logger_is_none():
    with patch.object(logging_network, 'setup_logging') as setup_logging:
        network = LoggingNetwork()
        setup_logging.assert_called_once_with(name=LoggingNetwork.LOGGER_NAME)
        assert network.logger is setup_logging.return_value


def test_logging_network_can_be_initialized_if_logger_is_none():
    with patch('logging.getLogger') as get_logger:
        get_logger.return_value = Mock(Logger)
        network = LoggingNetwork()
        assert network.logger is get_logger.return_value
        get_logger.assert_called_once_with(LoggingNetwork.LOGGER_NAME)


def test_logging_network_does_not_call_setup_logging_if_logger_is_not_none():
    logger = Mock(Logger)
    with patch.object(logging_network, 'setup_logging') as setup_logging:
        network = LoggingNetwork(logger)
        setup_logging.assert_not_called()
        assert network.logger is logger


def test_logging_network_logs_requests(http_verb, test_url, access_token):
    logger = Mock(Logger)
    network = LoggingNetwork(logger)
    with patch.object(logging_network, 'pformat') as pformat:
        with patch.object(default_network.DefaultNetwork, 'request') as super_request:
            network.request(http_verb, test_url, access_token, custom_kwarg='foo')
            kwargs = pformat.return_value
            super_request.assert_called_once_with(http_verb, test_url, access_token, custom_kwarg='foo')
            pformat.assert_called_once_with(dict(custom_kwarg='foo'))
    logger.info.assert_any_call(network.REQUEST_FORMAT, http_verb, test_url, kwargs)


def test_logging_network_logs_successful_responses(http_verb, test_url, access_token, generic_successful_response):
    logger = Mock(Logger)
    network = LoggingNetwork(logger)
    with patch.object(default_network.DefaultNetwork, 'request') as super_request:
        super_request.return_value = generic_successful_response
        network.request(http_verb, test_url, access_token)
        super_request.assert_called_once_with(http_verb, test_url, access_token)
    logger.info.assert_called_with(network.SUCCESSFUL_RESPONSE_FORMAT, generic_successful_response.content)


def test_logging_network_logs_non_successful_responses(http_verb, test_url, access_token, server_error_response):
    logger = Mock(Logger)
    network = LoggingNetwork(logger)
    with patch.object(logging_network, 'pformat') as pformat:
        with patch.object(default_network.DefaultNetwork, 'request') as super_request:
            super_request.return_value = server_error_response
            network.request(http_verb, test_url, access_token)
            super_request.assert_called_once_with(http_verb, test_url, access_token)
        pformat.assert_called_with(server_error_response.content)
    logger.warning.assert_called_once_with(
        network.ERROR_RESPONSE_FORMAT,
        server_error_response.status_code,
        server_error_response.headers,
        pformat.return_value,
    )
