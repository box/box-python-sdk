# coding: utf-8

from __future__ import absolute_import, unicode_literals

import io
import logging

from mock import mock_open, patch, Mock
import pytest
from six import string_types

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
            assert boxsdk.util.log.setup_logging(stream_or_file, debug=debug, name=name) == mock_logger
            get_logger.assert_called_once_with(name)

    assert mock_logger.addHandler.call_count == 1
    assert isinstance(mock_logger.addHandler.call_args[0][0], logging.Handler)
    mock_logger.setLevel.assert_called_once_with(expected_log_level)

    if isinstance(stream_or_file, string_types):
        assert mock_file_open.call_count == 1
        assert mock_file_open.call_args[0][:2] == (stream_or_file, 'w')   # Python 3 passes additional args.
