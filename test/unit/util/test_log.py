# coding: utf-8

import io
import logging

from mock import mock_open, patch, Mock
import pytest

import boxsdk.util.log


_MOCK_FILEPATH = '/home/user/boxsdk.log'
_MOCK_LOG_NAME = 'boxsdk'


@pytest.fixture(params=[io.StringIO(), _MOCK_FILEPATH])
def stream_or_file(request):
    return request.param


@pytest.fixture(params=[False, True])
def debug(request):
    return request.param


@pytest.fixture
def expected_log_level(debug):
    return logging.DEBUG if debug else logging.INFO


@pytest.fixture(params=[_MOCK_LOG_NAME, None])
def name(request):
    return request.param


@pytest.fixture
def mock_logger():
    return Mock(logging.Logger)


def test_setup_logging(stream_or_file, debug, expected_log_level, name, mock_logger):
    mock_file_open = mock_open()

    with patch('logging.getLogger') as get_logger:
        with patch('logging.open', mock_file_open, create=True):
            get_logger.return_value = mock_logger
            boxsdk.util.log.Logging().setup_logging(stream_or_file, debug=debug, name=name)
            get_logger.assert_called_once_with(name)

    assert mock_logger.addHandler.call_count == 1
    assert isinstance(mock_logger.addHandler.call_args[0][0], logging.Handler)
    mock_logger.setLevel.assert_called_once_with(expected_log_level)

    if isinstance(stream_or_file, str):
        assert mock_file_open.call_count == 1
        assert mock_file_open.call_args[0][:2] == (stream_or_file, 'a')   # Python 3 passes additional args.


def test_setup_logging_is_reentrant(mock_logger):
    mock_file_open = mock_open()

    with patch('logging.getLogger') as get_logger:
        with patch('logging.open', mock_file_open, create=True):
            get_logger.return_value = mock_logger
            logging_instance = boxsdk.util.log.Logging()
            logging_instance.setup_logging(None)
            get_logger.assert_called_once_with(None)
            get_logger.return_value = Mock()
            logging_instance.setup_logging(None)

    assert mock_logger.addHandler.call_count == 1
    assert isinstance(mock_logger.addHandler.call_args[0][0], logging.Handler)
    mock_logger.setLevel.assert_called_once()

    if isinstance(stream_or_file, str):
        assert mock_file_open.call_count == 1


@pytest.mark.parametrize(
    'unsanitized_dict, expected_result',
    [
        # Test for when no sanitization is required
        (
            {'name': 'foo'},
            {'name': 'foo'},
        ),
        # Test for basic string sanitization
        (
            {'access_token': 'askdjfhadsrwedr'},
            {'access_token': '---wedr'},
        ),
        # Test for short string sanitization
        (
            {'refresh_token': 'abc'},
            {'refresh_token': '---abc'},
        ),
        # Test for recursive sanitization
        (
            {'stuff': {'shared_link': 'https://example.com/asdfghjkl'}},
            {'stuff': {'shared_link': '---hjkl'}},
        ),
        # Test for None type
        (
            {'download_url': None},
            {'download_url': None},
        ),
    ]
)
def test_sanitize_dictionary_correctly_sanitizes_params(mock_logger, unsanitized_dict, expected_result):
    mock_file_open = mock_open()

    with patch('logging.getLogger') as get_logger:
        with patch('logging.open', mock_file_open, create=True):
            get_logger.return_value = mock_logger
            actual_result = boxsdk.util.log.Logging().sanitize_dictionary(unsanitized_dict)
            assert actual_result == expected_result
